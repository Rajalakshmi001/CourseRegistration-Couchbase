import { User } from './user.model';
import { Course } from './course.model';
import { Quarter } from './quarter.model';

export interface Db {
    currentQuarter: String;
    users: User[];
    courses: Course[];
    quarters: Quarter[];
    studentSchedules: String[][][];
}
