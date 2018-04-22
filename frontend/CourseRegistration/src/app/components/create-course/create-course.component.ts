import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { Http } from '@angular/http';
import { HttpClient } from 'selenium-webdriver/http';
import { Input } from '@angular/core';

@Component({
  selector: 'app-create-course',
  templateUrl: './create-course.component.html',
  styleUrls: ['./create-course.component.scss']
})
export class CreateCourseComponent implements OnInit {

  public form: FormGroup;
  public text = {
    name: 'Bill',
    display: false,
  };

  constructor(public http: Http) { }

  ngOnInit() {
    this.form = new FormGroup({
      name: new FormControl('', Validators.required),
      courseNumber: new FormControl('', Validators.required),
      description: new FormControl('', Validators.required),
    });

    this.http.get('http://137.112.89.91:5005/').subscribe(data => {
      console.log(data);
    });
  }

  public createCourse() {
    this.http.put('http://137.112.89.91:5005/course/1', {
      someData: 'my string',
      otherVar: 5
    }).subscribe(data => {
      console.log(data);
    });
  }

}
