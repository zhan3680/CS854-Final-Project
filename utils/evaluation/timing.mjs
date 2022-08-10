import * as c_p from 'child_process';

let __dirname = ""
const child1 = c_p.fork('request.mjs');
const child2 = c_p.fork('request.mjs');
const child3 = c_p.fork('request.mjs');
const child4 = c_p.fork('request.mjs');
const child5 = c_p.fork('request.mjs');
const child6 = c_p.fork('request.mjs');
const child7 = c_p.fork('request.mjs');
const child8 = c_p.fork('request.mjs');
const child9 = c_p.fork('request.mjs');
const child10 = c_p.fork('request.mjs');

// console.time('workflow')

child1.send('START 30');
child2.send('START 100');
child3.send('START 25');
child4.send('START 50');
child5.send('START 10');
child6.send('START 20');
child7.send('START 100');
child8.send('START 30');
child9.send('START 25');
child10.send('START 60');

child1.on('message', (message) => {
    console.log("child1 execution time: " + message)
})

child2.on('message', (message) => {
    console.log("child2 execution time: " + message)
})

child3.on('message', (message) => {
    console.log("child3 execution time: " + message)
})

child4.on('message', (message) => {
    console.log("child4 execution time: " + message)
})

child5.on('message', (message) => {
    console.log("child5 execution time: " + message)
})

child6.on('message', (message) => {
    console.log("child6 execution time: " + message)
})

child7.on('message', (message) => {
    console.log("child7 execution time: " + message)
})

child8.on('message', (message) => {
    console.log("child8 execution time: " + message)
})

child9.on('message', (message) => {
    console.log("child9 execution time: " + message)
})

child10.on('message', (message) => {
    console.log("child10 execution time: " + message)
})


// await new Promise( (resolve) => {
//     child1.on('close', resolve)
// })

// await new Promise( (resolve) => {
//     child2.on('close', resolve)
// })

// await new Promise( (resolve) => {
//     child3.on('close', resolve)
// })

// child1.on('exit', function() {
//     console.log("child1 exits");
// })

// child2.on('exit', function() {
//     console.log("child2 exits");
// })

// child3.on('exit', function() {
//     console.log("child3 exits");
// })

// console.timeEnd('workflow')