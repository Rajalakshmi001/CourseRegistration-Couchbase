import { OnInit, Component } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';

@Component({
    selector: 'app-create-offering',
    templateUrl: './create-offering.component.html',
    styleUrls: ['./create-offering.component.scss']
})
export class CreateOfferingComponent implements OnInit {

    public form: FormGroup;

    constructor() { }

    ngOnInit() {
        this.form = new FormGroup({
            proffessor: new FormControl(''),
            hour: new FormControl(''),
            capacity: new FormControl(0, Validators.min(0)),
            enrolled: new FormControl(0)
        });
    }

}
