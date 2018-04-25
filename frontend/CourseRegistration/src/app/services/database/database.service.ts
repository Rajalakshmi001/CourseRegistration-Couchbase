import { User } from './../../models/user.model';
import { Http } from '@angular/http';
import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';
import { NotificationService } from '../notification/notification.service';

@Injectable()
export class DatabaseService {

  constructor(private http: Http, private notificationService: NotificationService) { }

  getStudents(): Promise<User[]> {
    return new Promise((resolve, reject) => {
      this.http.get(`${environment.flaskRoot}/user`).subscribe(data => {
        const resp = JSON.parse(data['_body']);
        if (data.status === 200) {
          resolve(resp);
        }
      }, err => {
        this.notificationService.networkError(err);
        reject(err);
      });
    });
  }

}
