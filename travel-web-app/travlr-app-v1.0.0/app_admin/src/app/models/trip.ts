/**
 * Interface Trip instances are used to transfer HTML form data
 * to the component (and between components and REST endpoint) for rendering
 * by using the trip-data service (trip-data.service.ts).
 * NOTE :Angular will automatically convert JSON <=> JS objects
 */
export interface Trip {
    _id: string,  // Internal primary key in MongoDB
    code: string,
    name: string,
    length: string,
    start: Date,
    resort: string,
    perPerson: string,
    image: string,
    description: string
}