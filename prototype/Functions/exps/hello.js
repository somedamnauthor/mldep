/**
 * Hello world as an OpenWhisk action.
 */
function main(params) {
    var name = params.name || 'World';
    console.log(name)
    return {payload:  'Hello, ' + name + '!'};
}
