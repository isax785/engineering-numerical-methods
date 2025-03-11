def nc_function_args(settings, function, *args):
    """
    Convergence method applied to function with arguments:
    - settings:
        - 'tol': float, tolerance value to assess the convergence
        - 'delta': float, initial value for independent variable variation
        - 'delta_scaler': float, scaler value that divides the delta
        - 'x_0': float, initial value of independent variable
        - 'x_min': float, [opt.] minimum allowed value for independent variable
        - 'x_max': float, [opt.] maximum allowed value for independent variable
        - 'y_t': float, output variable target
        - 'trend': bool, default=None, function trend, monotonic increasing (True) or decreasing (False).
                    If None, the trend is assessed automatically.
        - 'count_max': int, maximum number of iterations
        - 'DEBUG': bool, enables debugging printouts
        - 'printout': print final result
    - function: function on which the convergence value must be reached. The function can
            be implemented on a single input or multiple ones. In case of multiple variables
            are needed by the function (i.e. len(args)>0) only the first one is varied to reach the convergence:
        - f(x) = y : single variable function
        - f(x1, x2, x3, ...) = y : multiple variables function
    - args: additional function inputs, they are not varied inside the convergence. 
            Not needed for single variable functions.
    """
    tol = settings.get('tol')
    delta = settings.get('delta')
    delta_scaler = settings.get('delta_scaler', 2)
    x = settings.get('x_0') # independent variable initialization
    x_min = settings.get('x_min')
    x_max = settings.get('x_max')
    y_t = settings.get('y_t')
    trend = settings.get('trend', None) 
    count_max = settings.get('count_max')
    DEBUG = settings.get('DEBUG', False)
    printout = settings.get('printout', False)

    def function_wrapper(function, x, args):
        if len(args) > 0:
            y = function(x, *args)
        else:
            y = function(x)
        return y

    if trend is None:
        "assess the trend of the function"
        y = function_wrapper(function, x, args)
        y_up = function_wrapper(function, x + delta, args)
        if y < y_up:
            "Monotonic Increasing with x"
            trend = True
        elif y > y_up:
            "Monotonic Decreasing with x"
            trend = False
        else:
            print(f"warning: the funciton trend for the given x {x} cannot be assessed. A Monotonic Increasing trend is assumed.")
            trend = True

    "initialization"
    inc = 1
    conv = False
    count = 1

    # if len(args) > 0:
    #     y = function(x, *args)
    # else:
    #     y = function(x)

    y = function_wrapper(function, x, args)
    
    while True:
        if DEBUG:
            print(f"{count} err: {abs(y - y_t):.4f} - x = {x:.4f} - y = {y:.4f} - y_t = {y_t:.4f}")
        if abs(y - y_t) <= tol:
            conv = True
            break

        count += 1
        if trend is True:
            "Monotonic Increasing with x"
            if y > y_t + tol:
                if inc == 1:
                    inc = -1
                    delta /= delta_scaler
                x -= delta
            elif y < y_t - tol:
                if inc == -1:
                    inc = 1
                    delta /= delta_scaler
                x += delta
        elif trend is False:
            "Monotonic Decreasing with x"
            if y < y_t - tol:
                if inc == 1:
                    inc = -1
                    delta /= delta_scaler
                x -= delta
            elif y > y_t + tol:
                if inc == -1:
                    inc = 1
                    delta /= delta_scaler
                x += delta
        
        "x limits"
        if x_min:
            if x < x_min: x = x_min
        if x_max:
            if x > x_max: x = x_max

        # if len(args) > 0:
        #     y = function(x, *args)
        # else:
        #     y = function(x)
        
        y = function_wrapper(function, x, args)

        if count_max:
            if count >= count_max:
                if DEBUG:
                    print("Iteration count limit reached. Exit the loop.")
                break
        
    if printout:
        if conv:
            print(f"Convergence reached!\n\tIterations: {count} - Error: {abs(y - y_t):.4f}\nx = {x:.4f} - y = {y:.4f} - y_t = {y_t:.4f}")
        else:
            print(f"Convergence not reached!\n\tIterations: {count} - Error: {abs(y - y_t):.4f}\nx = {x:.4f} - y = {y:.4f} - y_t = {y_t:.4f}")
    return x, y


def nc_function_dict(settings, function, inp_dict):
    """
    Convergence method applied to function dictionary (both input and output):
    - settings:
        - 'tol': float, tolerance value to assess the convergence
        - 'delta': float, initial value for independent variable variation
        - 'delta_scaler': float, scaler value that divides the delta
        - 'x_name': str, independent variable name (i.e. dictionary key)
        - 'x_0': float, initial value of independent variable
        - 'x_min': float, [opt.] minimum allowed value for independent variable
        - 'x_max': float, [opt.] maximum allowed value for independent variable
        - 'y_t_name': str, output variable name (i.e. dictionary key)
        - 'y_t': float, output variable target
        - 'trend': bool, default=None, function trend, monotonic increasing (True) or decreasing (False).
                    If None, the trend is assessed automatically.
        - 'count_max': int, maximum number of iterations
        - 'DEBUG': bool, enables debugging printouts
        - 'printout': print final result
    - function: function on which the convergence value must be reached. The function can
            be implemented on a single input or multiple ones. In case of multiple variables
            are needed by the function (i.e. len(args)>0) only the first one is varied to reach the convergence:
        - f(x) = y : single variable function
        - f(x1, x2, x3, ...) = y : multiple variables function
    - args: additional function inputs, they are not varied inside the convergence. 
            Not needed for single variable functions.
    """
    tol = settings.get('tol')
    delta = settings.get('delta')
    delta_scaler = settings.get('delta_scaler', 2)
    x_name = settings.get('x_name')
    x = settings.get('x_0') # independent variable initialization
    x_min = settings.get('x_min')
    x_max = settings.get('x_max')
    y_t_name = settings.get('y_t_name')
    y_t = settings.get('y_t')
    trend = settings.get('trend', None) 
    count_max = settings.get('count_max')
    DEBUG = settings.get('DEBUG', False)
    printout = settings.get('printout', False)

    def function_wrapper(function, inp_dict, x, x_name, y_t_name):
        inp_dict[x_name] = x
        res = function(inp_dict)
        y = res[y_t_name]
        return y
    
    if trend is None:
        "assess the trend of the function"
        y = function_wrapper(function, inp_dict, x, x_name, y_t_name)
        y_up = function_wrapper(function, inp_dict, x + delta, x_name, y_t_name)
        if y < y_up:
            "Monotonic Increasing with x"
            trend = True
        elif y > y_up:
            "Monotonic Decreasing with x"
            trend = False
        else:
            print(f"warning: the funciton trend for the given x {x} cannot be assessed. A Monotonic Increasing trend is assumed.")
            trend = True
    

    "initialization"
    inc = 1
    conv = False
    count = 1

    inp_dict[x_name] = x
    res = function(inp_dict)
    y = res[y_t_name]

    y = function_wrapper(function, inp_dict, x, x_name, y_t_name)
    
    while True:
        if DEBUG:
            print(f"{count} err: {abs(y - y_t):.4f} - x = {x:.4f} - y = {y:.4f} - y_t = {y_t:.4f}")
        if abs(y - y_t) <= tol:
            conv = True
            break

        count += 1
        if trend is True:
            "Monotonic Increasing with x"
            if y > y_t + tol:
                if inc == 1:
                    inc = -1
                    delta /= delta_scaler
                x -= delta
            elif y < y_t - tol:
                if inc == -1:
                    inc = 1
                    delta /= delta_scaler
                x += delta
        elif trend is False:
            "Monotonic Decreasing with x"
            if y < y_t - tol:
                if inc == 1:
                    inc = -1
                    delta /= delta_scaler
                x -= delta
            elif y > y_t + tol:
                if inc == -1:
                    inc = 1
                    delta /= delta_scaler
                x += delta
        
        "x limits"
        if x_min:
            if x < x_min: x = x_min
        if x_max:
            if x > x_max: x = x_max

        inp_dict[x_name] = x
        res = function(inp_dict)
        y = res[y_t_name]

        if count_max:
            if count >= count_max:
                if DEBUG:
                    print("Iteration count limit reached. Exit the loop.")
                break
    
    if printout:
        if conv:
            print(f"Convergence reached!\n\tIterations: {count} - Error: {abs(y - y_t):.4f}\nx ({x_name}) = {x:.4f} - y ({y_t_name}) = {y:.4f} - y_t = {y_t:.4f}")
        else:
            print(f"Convergence not reached!\n\tIterations: {count} - Error: {abs(y - y_t):.4f}\nx ({x_name}) = {x:.4f} - y ({y_t_name}) = {y:.4f} - y_t = {y_t:.4f}")
            
    return inp_dict, res