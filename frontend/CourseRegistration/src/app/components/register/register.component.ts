import { NotificationService } from './../../services/notification/notification.service';
import { environment } from './../../../environments/environment';
import { FormGroup, Validators, FormControl } from '@angular/forms';
import { Component, OnInit } from '@angular/core';
import { Pipe, PipeTransform } from '@angular/core';
import { Http } from '@angular/http';
import { Course } from '../../models/course.model';

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
  public quarters: { name: String, value: String }[];

  constructor(private http: Http, private notificationService: NotificationService) { }

  ngOnInit() {
    this.getCourses();
    this.form = new FormGroup({
      studentId: new FormControl('', Validators.required),
      courseId: new FormControl('', Validators.required),
      year: new FormControl('', Validators.required),
      quarter: new FormControl('', Validators.required),
    });

    this.students = [
      'metcalwd',
      'somasur',
      'dverlaque',
    ];

    this.courses = [ ];

    this.quarters = [
      { name: 'Spring', value: 'spring' },
      { name: 'Summer', value: 'summer' },
      { name: 'Fall', value: 'fall' },
      { name: 'Winter', value: 'winter' },
    ];

    this.years = [2017, 2018, 2019, 2020];
  }

  register() {
    console.log(this.form.value);
  }

  public getCourses() {
    this.http.get(`${environment.flaskRoot}/course`).subscribe(resp => {
      console.log(resp);
      if (resp.status === 200) {
        const data: Course[] = JSON.parse(resp['_body']);
        console.log(data);
        this.courses = data.map(val => val.courseNum);
      }
    }, err => {
      this.notificationService.networkError();
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
