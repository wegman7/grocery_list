function test() {
    f();
}

function outsideClosure() {
    let x = true;
    return function() {
        x = !x;
        console.log(x)
    }
}

let f = outsideClosure();
f();
f();
f();
f();
f();
f();