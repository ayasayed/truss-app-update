import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FixedsidnavComponent } from './fixedsidnav.component';

describe('FixedsidnavComponent', () => {
  let component: FixedsidnavComponent;
  let fixture: ComponentFixture<FixedsidnavComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FixedsidnavComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FixedsidnavComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
