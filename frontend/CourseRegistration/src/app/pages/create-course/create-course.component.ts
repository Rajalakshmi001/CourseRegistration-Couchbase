import { MatSnackBar } from '@angular/material/snack-bar';
import { environment } from './../../../environments/environment';
import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { Http } from '@angular/http';
import { HttpClient } from 'selenium-webdriver/http';
import { Input } from '@angular/core';
import { Course } from '../../models/course.model';
import { NotificationService } from '../../services/notification/notification.service';

@Component({
  selector: 'app-create-course',
  templateUrl: './create-course.component.html',
  styleUrls: ['./create-course.component.scss']
})
export class CreateCourseComponent implements OnInit {

  public form: FormGroup;

  constructor(public http: Http, private notificationService: NotificationService) { }

  ngOnInit() {
    this.form = new FormGroup({
      name: new FormControl('', Validators.required),
      courseNum: new FormControl('', Validators.required),
      description: new FormControl('', Validators.required),
    });
  }

  public createCourse() {
    const data: Course = this.form.value;
    this.http.put(`${environment.flaskRoot}/course/${data.courseNum}`, data).subscribe(resp => {
      console.log(resp);
      if (resp.status >= 200 && resp.status < 300) {
        this.notificationService.showSnackbar('Course Created!');
        this.form.reset();
      }
    }, err => {
      this.notificationService.showSnackbar('Failed to create course :(');
    });
  }

}
