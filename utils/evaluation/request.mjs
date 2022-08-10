import fetch from "node-fetch";
import openwhisk from "openwhisk";
import { exit } from "process";

async function get_CPU_usage(url) {
    let resp = await fetch(url);
    let a = await resp.text();
    return parseFloat(a);
}

// var a = await get_CPU_usage("http://20.25.181.174:9999");
// console.log(a);


async function select_invoker() {
        let a = await get_CPU_usage("http://20.25.181.174:9999"); // server_2 usage
        let b = await get_CPU_usage("http://20.25.166.36:9999"); // server_3 usage
        if (a >= b) {
            return "20.25.166.36";
        } else {
            return "20.25.181.174";
        }
    
}
// console.log('1');
// console.log(await select_invoker());
// console.log('2');

async function invoke(my_apihost, action_name, params){
    const my_auth = '23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP'
    var options = {apihost: my_apihost, api_key: my_auth, ignore_certs: true};
    console.log(options, params, action_name);
    var ow = openwhisk(options);

    const blocking = true; 
    const result = true;
    const name = action_name;
    return ow.actions.invoke({name, blocking, result, params});
}

// var name = 'linear';
// var my_apihost = '20.25.181.174';
// var params = {'n': 10}; 
// var a = await invoke(my_apihost, name, params);
// var b = new Map(Object.entries(a))
// console.log(typeof(b));
// var name1 = "cubic";
// var b = await invoke(my_apihost, name1, a);
// console.log(b);


const workflow_individual_functions = ['constant', 'logarithmic', 'linear', 'linearithmic', 'quadratic', 'cubic'] //normal openwhisk workflow
const workflow_hybrid = ['faastlane_time_complexity_part1', 'cubic'] // Faastlane generated sub-workflows
const workflow_faastlane = ['faastlane_time_complexity']

async function run_workflow(input_n, workflow) {
    var params = {'n': input_n};
    var my_apihost;
    for (let id in workflow) {
        my_apihost = await select_invoker();
        params = await invoke(my_apihost, workflow[id], params);
    }
    
    return params;
}

// var my_apihost = await select_invoker();
// var params = {'n': 10};
// var res = await invoke(my_apihost, 'linear', params);
// console.log(res);

// console.log(await run_workflow(10, workflow1));

// async function run_faastlane_workflow(input_n) {
//     var params = {'n': input_n};
//     var my_apihost = '20.25.181.174';
//     var faastlane_workflow_name = 'faastlane_time_complexity';

//     return invoke(my_apihost, faastlane_workflow_name, params);
// }


process.on('message', async (message) => {
    var messages = message.split(' ')
    if (messages[0] == 'START') {
      var start = Date.now();
      //console.log('Child process received START message');
      let slowResult = await run_workflow(parseInt(messages[1]), workflow_hybrid);
    //   let slowResult = await run_faastlane_workflow(parseInt(messages[1]));
      var finish = Date.now();
      var execution_time = finish-start;
      process.send(`${execution_time}`);
      process.exit(0);
    }
});