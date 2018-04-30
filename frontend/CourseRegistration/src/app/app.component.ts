import { Component, HostListener } from '@angular/core';
import { DeviceService } from './services/device/device.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {

  public sidebarOpen = false;
  public isMobile: boolean;

  constructor(public device: DeviceService) {
    this.isMobile = this.device.isMobile;

    document.ontouchmove = function (event) {
      event.preventDefault();
    };
  }

  @HostListener('window:resize', ['$event'])
  onResize(event) {
    this.isMobile = this.device.isMobile;
  }

  public toggleSidebar() {
    this.sidebarOpen = !this.sidebarOpen;
  }
}
