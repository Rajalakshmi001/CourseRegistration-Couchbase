import { OnInit, Component } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';

@Component({
    selector: 'app-create-offering',
    templateUrl: './create-offering.component.html',
    styleUrls: ['./create-offering.component.scss']
})
export class CreateOfferingComponent implements OnInit {

    public form: FormGroup;
    public professors: { name: string, value: string }[];
    public courses: { name: string, value: string }[];
    public quarters: { name: string, value: string }[];
    public hours: number[];

    constructor() { }

    ngOnInit() {
        this.form = new FormGroup({
            professor: new FormControl('', Validators.required),
            course: new FormControl('', Validators.required),
            quarter: new FormControl('', Validators.required),
            hour: new FormControl('', Validators.required),
            capacity: new FormControl(0, Validators.min(0)),
            enrolled: new FormControl(0)
        });

        this.professors = [
            { name: 'Sriram', value: 'key1' },
            { name: 'Boutell', value: 'key2' },
        ];

        this.quarters = [
            { name: 'Spring 2018', value: 'q1' }
        ];

        this.courses = [
            { name: 'CSSE 433', value: 'c1' }
        ];

        this.hours = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    }

    createOffering() {
        console.log(this.form.value);
    }
}
