import { Injectable } from '@angular/core';

@Injectable()
export class DeviceService {

  constructor() { }

  get isMobile(): boolean {
    return Math.min(window.innerWidth, window.innerHeight) <= 500;
  }

}
