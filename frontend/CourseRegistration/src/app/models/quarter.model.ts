import { Offering } from './offering.model';

export interface Quarter {
    courseInfo: String[]; // courseId -> course name
    courses: Offering[];
}
