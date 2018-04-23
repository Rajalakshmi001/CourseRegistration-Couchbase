import { CreateOfferingComponent } from './components/create-offering/create-offering.component';
import { CreateCourseComponent } from './components/create-course/create-course.component';
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { UserPageComponent } from './components/user-page/user-page.component';
import { CreateUserComponent } from './components/create-student/create-student.component';
import { RegisterComponent } from './components/register/register.component';
import { LookupComponent } from './components/lookup/lookup.component';

const routes: Routes = [{
  path: 'user',
  component: UserPageComponent,
},
{
  path: 'create-course',
  component: CreateCourseComponent,
},
{
  path: 'create-offering',
  component: CreateOfferingComponent,
},
{
  path: 'create-user',
  component: CreateUserComponent,
},
{
  path: 'register',
  component: RegisterComponent,
},
{
  path: 'lookup',
  component: LookupComponent,
}];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
