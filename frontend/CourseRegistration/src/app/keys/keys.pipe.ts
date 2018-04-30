import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'keys' })
export class KeysPipe implements PipeTransform {
  transform(value: string[], keyword: string): string[] {
    if (!value) {
      return [];
    }
    const ret = [];
    for (const val in value) {
        let data: any;
        if (typeof value[val] === 'object') {
            data = value[val];
        } else {
            data = {
                value: value[val]
            };
        }
        data['$fromKey'] = val;
        ret.push(data);
    }
    return ret;
  }
}
