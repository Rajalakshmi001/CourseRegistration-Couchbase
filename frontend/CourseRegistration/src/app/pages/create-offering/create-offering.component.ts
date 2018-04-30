import { Http } from '@angular/http';
import { Offering } from './../../models/offering.model';
import { OnInit, Component } from '@angular/core';
import { FormGroup, FormControl, Validators, FormArray } from '@angular/forms';
import { DatabaseService } from '../../services/database/database.service';
import { NotificationService } from '../../services/notification/notification.service';
import { environment } from '../../../environments/environment';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
    selector: 'app-create-offering',
    templateUrl: './create-offering.component.html',
    styleUrls: ['./create-offering.component.scss']
})
export class CreateOfferingComponent implements OnInit {

    public form: FormGroup;
    public professors: { name: String, value: String }[];
    public courses: { name: String, value: String }[];
    public quarters: { name: String, value: String }[];
    public days: { name: String, value: number }[];
    public years: number[];
    public hours: number[];

    constructor(private http: Http,
        private db: DatabaseService,
        private notificationService: NotificationService) { }

    ngOnInit() {
        this.getCourses();
        this.createForm();
        this.professors = [
            { name: 'Sriram', value: 'key1' },
            { name: 'Boutell', value: 'key2' },
        ];

        this.quarters = [
            { name: 'Spring', value: 'spring' },
            { name: 'Summer', value: 'summer' },
            { name: 'Fall', value: 'fall' },
            { name: 'Winter', value: 'winter' },
        ];

        this.years = [2017, 2018, 2019, 2020];

        this.courses = [];

        this.days = [
            { name: 'Monday', value: 0 },
            { name: 'Tuesday', value: 1 },
            { name: 'Wednesday', value: 2 },
            { name: 'Thursday', value: 3 },
            { name: 'Friday', value: 4 },
        ];

        this.hours = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    }

    private createForm() {
        this.form = new FormGroup({
            prof: new FormControl('', Validators.required),
            courseNum: new FormControl('', Validators.required),
            quarter: new FormControl('spring', Validators.required),
            year: new FormControl(2018, Validators.required),
            hour: new FormControl('', Validators.required),
            days: new FormControl([], Validators.required),
            capacity: new FormControl(0, Validators.min(0)),
            enrolled: new FormControl(0, Validators.required),
            offeringId: new FormControl(1, Validators.required),
        });
    }

    getCourses() {
        this.db.getCourses().then(courses => {
            this.courses = courses.map(val => {
                return { name: val.name, value: val.courseNum };
            });
        });
    }

    createOffering() {
        const data = this.form.value;
        const offering: Offering = {
            courseNum: data.courseNum,
            enrolled: data.enrolled,
            capacity: data.capacity,
            hour: data.hour,
            days: data.days,
            prof: data.prof,
            quarter: data.quarter + data.year,
            offeringId: data.offeringId,
        };
        console.log(offering);
        this.http.put(`${environment.flaskRoot}/offering/${offering.quarter}/${offering.courseNum}/${offering.offeringId}`,
            offering).subscribe(resp => {
                if (resp.status >= 200 && resp.status < 300) {
                    this.notificationService.showSnackbar('Offering Created!');
                    // this.form.reset();
                    this.createForm();
                }
            }, err => {
                console.error(err);
                this.notificationService.showSnackbar('Failed To Create Offering :(');
            });
    }
}
