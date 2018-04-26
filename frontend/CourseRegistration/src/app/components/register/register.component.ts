import { NotificationService } from './../../services/notification/notification.service';
import { environment } from './../../../environments/environment';
import { FormGroup, Validators, FormControl } from '@angular/forms';
import { Component, OnInit } from '@angular/core';
import { Pipe, PipeTransform } from '@angular/core';
import { Http } from '@angular/http';
import { Course } from '../../models/course.model';
import { DatabaseService } from '../../services/database/database.service';

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

  constructor(private http: Http, private notificationService: NotificationService, private db: DatabaseService) { }

  ngOnInit() {
    this.getCourses();
    this.getStudents();
    this.form = new FormGroup({
      studentId: new FormControl('', Validators.required),
      courseNum: new FormControl('', Validators.required),
      year: new FormControl('', Validators.required),
      quarter: new FormControl('', Validators.required),
      offeringId: new FormControl('', Validators.required),
    });

    this.students = [];

    this.courses = [];

    this.offerings = [];

    this.quarters = [
      { name: 'Spring', value: 'spring' },
      { name: 'Summer', value: 'summer' },
      { name: 'Fall', value: 'fall' },
      { name: 'Winter', value: 'winter' },
    ];

    this.years = [2017, 2018, 2019, 2020];

    this.form.valueChanges.subscribe(data => {
      console.log(data);
      if (data && data.courseNum && data.year && data.quarter) {
        // pull offerings
        this.getOfferings(data.courseNum, data.year, data.quarter);
        console.log('ready');
      }
    });
  }

  register() {
    console.log(this.form.value);
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
      console.log(data);
    }).catch(err => {
      console.error(err);
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
