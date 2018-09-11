
function isInflectionPoint(func, dot){
    let flag
    // i.e. "f(x) = x⁷ + x⁶ - x⁵ + x⁴ - x³ - x²"
    let my_func = ggbApplet.evalCommandGetLabels(func)
    // i.e. "A = (-1.3, 5.6279873)"
    let point = ggbApplet.evalCommandGetLabels(dot)
    
    // f(x) == y
    ggbApplet.evalCommand(`j = ${my_func}(x(${point}))`)
    console.log(`f(x(A)) = ${ggbApplet.getValue(`f(x(${point}))`)}`)    
    ggbApplet.evalCommand(`i = y(${point})`)
    console.log(`y(A) = ${ggbApplet.getValue(`y(${point})`)}`)
    ggbApplet.getValue('i').toFixed(3) === ggbApplet.getValue('j').toFixed(3)
    ?
    flag = true
    :
    flag = false

    if(!flag) return false

    // p
    let dev_func = ggbApplet.evalCommandGetLabels(`Derivative(${my_func}, 2)`)
    console.log(`Derivative: ${dev_func}`);
    
    let derivative = ggbApplet.evalCommandGetLabels(dev_func)
    console.log(`Derviative Function: ${ggbApplet.getValueString(derivative)}`)

    // "H,I,J"
    let roots = ggbApplet.evalCommandGetLabels(ggbApplet.evalCommandCAS(`Roots(${derivative}, -2, 1)`))
    console.log(`Roots label(s) : ${roots}`)
    roots.split(",").map(item => console.log(ggbApplet.getValueString(item)))
    
    // "-1.3"
    let point_to_find = ggbApplet.getValue(`x(${point})`)
    console.log(`x to Find : ${point_to_find}`)

    // ["H = (-1.3, 0)"]
    let found_points = roots.split(",").map(item => ggbApplet.getValueString(item)).filter(item => item.includes(point_to_find))
    found_points.length > 0 ? console.log(`Points Found : ${found_points}`) : console.log('No Match')

    found_points.length > 0
    ?
    flag = true
    :
    flag = false 
    
    if(!flag) {
        console.log(`(x=${point_to_find}) not in ${roots.split(",").map(item => ggbApplet.getValueString(item))}`)
        return false
    }

    ggbApplet.evalCommand(`o = ${derivative}(x+0.001)`)
    ggbApplet.evalCommand(`u = ${derivative}(x-0.001)`)

    ggbApplet.evalCommand(`c1 = o(x(${point}))`)
    ggbApplet.evalCommand(`c2 = u(x(${point}))`)

    ggbApplet.getValue('c1').toFixed(3) === ggbApplet.getValue('c2').toFixed(3)
    ?
    flag = true
    :
    flag = false

    return flag
}
