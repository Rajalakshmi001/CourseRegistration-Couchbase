import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateOfferingComponent } from './create-offering.component';

describe('CreateOfferingComponent', () => {
  let component: CreateOfferingComponent;
  let fixture: ComponentFixture<CreateOfferingComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CreateOfferingComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CreateOfferingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
