export interface Offering {
    enrolled: Number;
    capacity: Number;
    hour: (1 | 2 | 3 | 4 | 5 | 6 | 7 | 9 | 10);
    days: (0 | 1 | 2 | 3 | 4)[];
    prof: String;
    courseNum: String;
    quarter: String;
    offeringId: Number;
}
