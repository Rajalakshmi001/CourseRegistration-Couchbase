import { User } from './../../models/user.model';
import { Http } from '@angular/http';
import { Injectable } from '@angular/core';
import { NotificationService } from '../notification/notification.service';
import { Course } from '../../models/course.model';
import { Offering } from '../../models/offering.model';
import { environment } from '../../../environments/environment';

@Injectable()
export class DatabaseService {

  constructor(private http: Http, private notificationService: NotificationService) { }

  public getStudents(): Promise<User[]> {
    console.log('GET -- /user/');
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

  public getCourses(): Promise<Course[]> {
    console.log('GET -- /course/');
    return new Promise((resolve, reject) => {
      this.http.get(`${environment.flaskRoot}/course`).subscribe(data => {
        if (data.status === 200) {
          const resp: Course[] = JSON.parse(data['_body']);
          resolve(resp);
        }
      }, err => {
        this.notificationService.networkError();
        reject(err);
      });
    });
  }

  public getOfferings(courseNum: String, quarter: String, offeringId: String = ''): Promise<Offering[]> {
    console.log(`GET -- /offering/${quarter}/${courseNum}${offeringId ? '/' + offeringId : ''}`);
    return new Promise((resolve, reject) => {
      this.http.get(`${environment.flaskRoot}/offering/${quarter}/${courseNum}${offeringId ? '/' + offeringId : ''}`).subscribe(data => {
        if (data.status === 200) {
          const resp: Offering[] = JSON.parse(data['_body']);
          resolve(resp);
        } else if (data.status === 204) {
          resolve([]);
        }
      }, err => {
        this.notificationService.networkError();
        reject(err);
      });
    });
  }

}
