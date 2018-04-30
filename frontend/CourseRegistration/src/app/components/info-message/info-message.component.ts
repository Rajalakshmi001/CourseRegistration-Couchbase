import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-info-message',
  templateUrl: './info-message.component.html',
  styleUrls: ['./info-message.component.scss']
})
export class InfoMessageComponent implements OnInit {

  @Input() message: String = '';
  @Input() type: 'warning' | 'error' | 'success' | '' = '';
  constructor() { }

  ngOnInit() {
  }

}
