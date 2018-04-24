import { Injectable } from '@angular/core';

@Injectable()
export class DeviceService {

  constructor() { }

  get isMobile(): boolean {
    return window.innerWidth <= 600;
  }

}
