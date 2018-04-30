import { DatabaseService } from './../../services/database/database.service';
import { environment } from './../../../environments/environment';
import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { MatTableDataSource } from '@angular/material/table';
import { Http } from '@angular/http';
import { NotificationService } from '../../services/notification/notification.service';

@Component({
  selector: 'app-lookup',
  templateUrl: './lookup.component.html',
  styleUrls: ['./lookup.component.scss']
})
export class LookupComponent implements OnInit {

  public form: FormGroup;
  public schedule: any;
  public students: String[];
  public quarters: { name: String, value: String }[];
  public years: number[];
  public rawSchedule: any;
  public courseData: any;

  constructor(private http: Http, private notificationService: NotificationService, private db: DatabaseService) {
  }

  ngOnInit() {
    this.getStudents();
    this.form = new FormGroup({
      studentId: new FormControl('', Validators.required),
      year: new FormControl(2018, Validators.required),
      quarter: new FormControl('spring', Validators.required)
    });

    this.form.valueChanges.subscribe(data => {
      if (this.form.valid) {
        this.buildSchedule(data);
      }
    });

    this.students = [];
    this.years = [2017, 2018, 2019, 2020];
    this.quarters = [
      { name: 'Spring', value: 'spring' },
      { name: 'Summer', value: 'summer' },
      { name: 'Fall', value: 'fall' },
      { name: 'Winter', value: 'winter' },
    ];
  }

  private buildSchedule(data) {
    const sched = [
      { 1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: '', 10: '' },
      { 1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: '', 10: '' },
      { 1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: '', 10: '' },
      { 1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: '', 10: '' },
      { 1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: '', 10: '' },
    ];

    this.http.get(`${environment.flaskRoot}/lookup/${data.studentId}/${data.quarter}${data.year}`).subscribe(resp => {
      const respData = JSON.parse(resp['_body']);
      console.log(respData);
      if (!respData) {
        return;
      }
      this.rawSchedule = respData.offerings;
      const offeringCallbacks = [];
      for (const courseNum in this.rawSchedule) {
        offeringCallbacks.push(this.db.getOfferings(courseNum, data.quarter + data.year, this.rawSchedule[courseNum]));
      }
      Promise.all(offeringCallbacks).then(offeringResponses => {
        this.courseData = {};
        for (const off in offeringResponses) {
          this.courseData[offeringResponses[off].courseNum] = offeringResponses[off];
        }

        for (const course in this.courseData) {
          const c = this.courseData[course];
          for (const day in c.days) {
            const num = c.days[day];
            sched[num][c.hour] = c.courseNum;
          }
        }
        this.schedule = new MatTableDataSource(sched);
      }).catch(err => {
        console.error(err);
      });
    }, err => {
      console.error(err);
    });

  }

  getStudents() {
    this.db.getStudents().then(students => {
      this.students = students.map(val => val.username);
    });
  }

  dropClass(classData: { value: string, '$fromKey': string }) {
    const formVal = this.form.value;
    const quarterId = formVal.quarter + formVal.year;
    this.http.delete(`${environment.flaskRoot}/register`, {
      body: {
        quarterId,
        courseNum: classData.$fromKey,
        offeringId: classData.value,
        studentId: formVal.studentId
      }
    }).subscribe(resp => {
      console.log(resp);
      this.buildSchedule(formVal);
    }, err => {
      console.error(err);
    });
  }
}
