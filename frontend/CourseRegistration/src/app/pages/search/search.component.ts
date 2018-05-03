import { environment } from './../../../environments/environment';
import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { Http } from '@angular/http';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent implements OnInit {

  public form: FormGroup;
  public results: any[];
  constructor(private http: Http) { }

  ngOnInit() {
    this.form = new FormGroup({
      department: new FormControl(''),
      queryString: new FormControl('')
    });
  }

  search() {
    const data = this.form.value;

    this.http.post(`${environment.flaskRoot}/search`, data).subscribe(resp => {
      console.log(resp);
      if (resp.status >= 200 && resp.status < 300) {
          this.results = JSON.parse(resp['_body']);
      }
    }, err => {
      console.error(err);
    });
  }

}
