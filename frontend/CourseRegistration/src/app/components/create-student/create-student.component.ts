import { FormGroup, FormControl, Validators } from '@angular/forms';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-create-student',
  templateUrl: './create-student.component.html',
  styleUrls: ['./create-student.component.scss']
})
export class CreateStudentComponent implements OnInit {

  public form: FormGroup;

  constructor() { }

  ngOnInit() {
    this.form = new FormGroup({
      username: new FormControl('', Validators.required),
      name: new FormControl('', Validators.required),
      courses: new FormControl([]),
    });
  }

  createStudent() {
    console.log(this.form.value);
  }

}
