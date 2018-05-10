import { NotificationService } from './../../services/notification/notification.service';
import { environment } from './../../../environments/environment';
import { FormGroup, Validators, FormControl } from '@angular/forms';
import { Component, OnInit } from '@angular/core';
import { Pipe, PipeTransform } from '@angular/core';
import { Http } from '@angular/http';
import { Course, CourseTaken } from '../../models/course.model';
import { DatabaseService } from '../../services/database/database.service';
import * as _ from 'lodash';
import { MatSnackBar, MatSnackBarRef, SimpleSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {

  public form: FormGroup;
  public students: String[];
  public courses: String[];
  public years: number[];
  public offerings: String[];
  public quarters: { name: String, value: String }[];
  public lastVal: any;
  public recommendedCourses: any[] = [
    {courseNum: 'course1'},
    {courseNum: 'course2'}
  ];

  constructor(private http: Http,
    private notificationService: NotificationService,
    private db: DatabaseService) { }

  ngOnInit() {
    this.getCourses();
    this.getStudents();
    this.form = new FormGroup({
      studentId: new FormControl('', Validators.required),
      courseNum: new FormControl('', Validators.required),
      year: new FormControl(2018, Validators.required),
      quarter: new FormControl('spring', Validators.required),
      offeringId: new FormControl('', Validators.required),
    });

    this.lastVal = _.clone(this.form.value);
    this.form.get('offeringId').disable();

    this.students = [];
    this.courses = [];
    this.offerings = null;
    this.quarters = [
      { name: 'Spring', value: 'spring' },
      { name: 'Summer', value: 'summer' },
      { name: 'Fall', value: 'fall' },
      { name: 'Winter', value: 'winter' },
    ];
    this.years = [2017, 2018, 2019, 2020];

    this.form.valueChanges.subscribe(data => {
      if (!data.offeringId) {
        data.offeringId = '';
      }
      const requiredValuesEnter = data && data.courseNum && data.year && data.quarter;
      const formDataChanged = !_.isEqual(data, this.lastVal);
      this.lastVal = data;

      if (requiredValuesEnter && formDataChanged) {
        this.getOfferings(data.courseNum, data.year, data.quarter);
      } else if (formDataChanged) {
        this.offerings = null;
        this.form.get('offeringId').disable();
      }
    });

    this.form.get('studentId').valueChanges.subscribe(data => {
      console.log(data);
      this.getRecommendations(data);
    });
  }

  private getRecommendations(val) {
    this.http.get(`${environment.flaskRoot}/recommend/${val}`).subscribe(resp => {
      console.log(resp);
      this.recommendedCourses = JSON.parse(resp['_body']);
      console.log(this.recommendedCourses);
    }, error => {
      console.error(error);
    });
  }

  register() {
    const data = _.clone(this.form.value);
    data.quarterId = data.quarter + data.year;
    delete data.quarter;
    delete data.year;
    console.log('PUT -- /register/', data);
    this.http.put(`${environment.flaskRoot}/register`, data).subscribe(resp => {
      if (resp.status >= 200 && resp.status < 300) {
        this.notificationService.showSnackbar(`Successfully registered ${data.studentId} for ${data.courseNum}-${data.offeringId}`);
      }
    }, err => {
      if (err.status === 304) {
        this.notificationService.showSnackbar('User is already registered for this course :(');
      } else {
        console.error(err);
        this.notificationService.showSnackbar('An unknown error occured :(');
      }
    });
  }

  getStudents() {
    this.db.getStudents().then(students => {
      this.students = students.map(val => val.username);
    });
  }

  getCourses() {
    this.db.getCourses().then(courses => {
      this.courses = courses.map(val => val.courseNum);
    });
  }

  getOfferings(courseNum: String, year: Number, quarter: String) {
    const q = quarter + String(year);
    this.db.getOfferings(courseNum, q).then(data => {
      if (data) {
        this.form.get('offeringId').enable();
        this.offerings = data.map(val => `${val.offeringId}`);
      } else {
        this.offerings = [];
        this.form.get('offeringId').disable();
        this.notificationService.showSnackbar('No offerings currently exist for this course/time :(');
      }
    }).catch(err => {
      console.error(err);
      this.notificationService.networkError(err);
    });
  }
}

@Pipe({ name: 'filterPipe' })
export class FilterPipe implements PipeTransform {
  transform(value: string[], keyword: string): string[] {

    if (!value || !value.length) {
      return [];
    }

    return value.filter((val) => {
      return val.includes(keyword);
    });
  }
}
