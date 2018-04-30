import { User } from './../../models/user.model';
import { environment } from './../../../environments/environment';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { Component, OnInit } from '@angular/core';
import { Http } from '@angular/http';
import { MatSnackBar } from '@angular/material/snack-bar';
import { NotificationService } from '../../services/notification/notification.service';

@Component({
  selector: 'app-create-student',
  templateUrl: './create-student.component.html',
  styleUrls: ['./create-student.component.scss']
})
export class CreateUserComponent implements OnInit {

  public form: FormGroup;

  constructor(private http: Http, private notificationService: NotificationService) { }

  ngOnInit() {
    this.createForm();
  }

  createForm() {
    this.form = new FormGroup({
      username: new FormControl('', Validators.required),
      name: new FormControl('', Validators.required),
      type: new FormControl('', Validators.required),
      courses: new FormControl([]),
    });
  }

  createStudent() {
    const data: User = this.form.value;
    this.http.put(`${environment.flaskRoot}/user/${data.username}`, data).subscribe(resp => {
      if (resp.status >= 200 && resp.status < 300) {
        this.notificationService.showSnackbar('User Created!');
        this.form.reset();
        this.form.markAsPristine();
        this.form.updateValueAndValidity();
      }
    }, err => {
      if (err.status === 304) {
        this.notificationService.showSnackbar('Username already exists :(');
      } else {
        this.notificationService.showSnackbar('An unkown error occured :(');
      }
    });
  }
}
