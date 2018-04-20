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
    class: ['333', '433'],
    display: false,
  };

  constructor(public http: Http) { }

  ngOnInit() {
    this.form = new FormGroup({
      name: new FormControl('', Validators.required),
    });

    this.http.get('http://137.112.89.91:5005/').subscribe(data => {
      console.log(data);
    });
  }

}
