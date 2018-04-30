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
      username: new FormControl('', Validators.required),
      year: new FormControl('', Validators.required),
      quarter: new FormControl('', Validators.required)
    });

    this.courseData = {};

    this.rawSchedule = [
      { courseId: 'csse433', offeringId: 'offeringKey1' },
      { courseId: 'csse333', offeringId: 'offeringKey2' },
    ];

    this.courseData['offeringKey1'] = {
      enrolled: 0,
      capacity: 0,
      hour: 2,
      days: [0, 2, 3],
      prof: '',
      name: 'csse433',
    };

    this.courseData['offeringKey2'] = {
      enrolled: 0,
      capacity: 0,
      hour: 4,
      days: [1, 4],
      prof: '',
      name: 'csse333',
    };

    const sched = [
      { 1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: '', 10: '' },
      { 1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: '', 10: '' },
      { 1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: '', 10: '' },
      { 1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: '', 10: '' },
      { 1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: '', 10: '' },
    ];

    // tslint:disable-next-line:forin
    for (const course in this.courseData) {
      const data = this.courseData[course];
      // tslint:disable-next-line:forin
      for (const day in data.days) {
        const num = data.days[day];
        sched[num][data.hour] = data.name;
      }
    }

    this.schedule = new MatTableDataSource(sched);

    this.students = [];
    this.years = [2017, 2018, 2019, 2020];
    this.quarters = [
      { name: 'Spring', value: 'spring' },
      { name: 'Summer', value: 'summer' },
      { name: 'Fall', value: 'fall' },
      { name: 'Winter', value: 'winter' },
    ];
  }

  getStudents() {
    this.db.getStudents().then(students => {
      this.students = students.map(val => val.username);
    });
  }

}
