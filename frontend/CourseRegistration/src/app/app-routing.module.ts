import { CreateOfferingComponent } from './components/create-offering/create-offering.component';
import { CreateCourseComponent } from './components/create-course/create-course.component';
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { UserPageComponent } from './components/user-page/user-page.component';

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
}];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
