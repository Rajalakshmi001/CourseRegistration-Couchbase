import { MatSnackBar } from '@angular/material/snack-bar';
import { environment } from './../../../environments/environment';
import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { Http } from '@angular/http';
import { HttpClient } from 'selenium-webdriver/http';
import { Input } from '@angular/core';
import { Course } from '../../models/course.model';

@Component({
  selector: 'app-create-course',
  templateUrl: './create-course.component.html',
  styleUrls: ['./create-course.component.scss']
})
export class CreateCourseComponent implements OnInit {

  public form: FormGroup;

  constructor(public http: Http, private snackbar: MatSnackBar) { }

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
      if (resp.status === 200) {
        this.snackbar.open('Course Created!', 'OK', { duration: 2000 });
        this.form.reset();
      }
    }, err => {
      this.snackbar.open('Failed to create course :(', 'OK', { duration: 2000 });
    });
  }

}
