import { FormGroup, Validators, FormControl } from '@angular/forms';
import { Component, OnInit } from '@angular/core';
import { Pipe, PipeTransform } from '@angular/core';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {

  public form: FormGroup;
  public students: string[];
  public courses: string[];
  public years: number[];
  public quarters: { name: string, value: string }[];

  constructor() { }

  ngOnInit() {
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

    this.courses = [
      'CSSE433',
      'CSSE333',
    ];

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
