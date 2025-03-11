from CoolProp.CoolProp import PropsSI
import CoolProp.CoolProp as CP
import matplotlib.pyplot as plt

"""
NOTE: measurement unit used at the interface with these functions
      - p: float, absolute pressure [bar]
      - t: float, temperature [degC]
      - x: float, quality [0-1]
      - h: float, specific enthalpy [J/kg/K]
"""

def propssi_usage_exaples():
    "Prints some PropsSI usage examples"
    s = "--- PropsSI Usage Examples ---"
    s += "P critical value       -> PropsSI('Pcrit', 'refrigerant')\n"
    s += "P from T/Q (dew point) -> PropsSI('P', 'T', 300, 'Q', 1, 'refrigerant')\n"
    print(s)

def measurement_units():
    "Prints the measurement units of the mostly used magnitudes for refrigerants"
    s = "--- Refrigerant Measurement Units ---"
    s += "P: [Pa] (absolute!)\n"
    s += "T: [K]\n"
    s += "H: [J/kg/K]\n"
    print(s)

def critical_point(ref:str):
    """
    Printout of the Critical Point properties
    - ref: str, refrigerant id for CoolProp
    """
    print(f"P Crit: {PropsSI('Pcrit', ref) / 1e5:2f} bar")
    print(f"T Crit: {PropsSI('Tcrit', ref) - 273.15:2f} degC")

def calc_h(point:list, ref:str):
    """
    Calculation of enthalpy given a point
    - point: list[float]
        - p: float, relative pressure [barg]
        - t: float, temperature [degC]
        - x: float, vapour quality [0-1]
    - ref: str, refrigerant id for CoolProp
    Return
    - p: float, absolute pressure [bar]
    - t: float, temperature [degC]
    - x: float, quality [0-1]
    - h: float, specific enthalpy [J/kg/K]
    """
    if len(point) == 2:
        # correction of the point to have all the 3 required values
        point.append(None)
    p, t, x = point
    if p is not None and t is not None:
        p += 1 # from relative to absolute pressure
        h = PropsSI('H', 'P', p * 1e5, 'T', t + 273.15, ref)
        x = PropsSI('Q', 'P', p * 1e5, 'T', t + 273.15, ref)
    elif p is None and t is not None and x is not None:
        h = PropsSI('H', 'T', t + 273.15, 'Q', x ,ref)
        p = PropsSI('P', 'T', t + 273.15, 'H', h, ref)
    elif p is not None and t is None and x is not None:
        p += 1 # from relative to absolute pressure
        h = PropsSI('H', 'P', p * 1e5, 'Q', x, ref)
        t = PropsSI('T', 'P', p * 1e5, 'Q', x, ref) - 273.15
    else:
        raise ValueError("The given point {point} is not well defined")
    # print(p, t, h) # DEBUG
    return p, t, x, h

def ph_diagram(ref, points=[], pcrit=None, tcrit=None, plot_settings={}):
    """
    Drawing of a single or multiple thermodynamic cycles into the refrigerant ph diagram.
    - ref: str, refrigerant CoolProp id
    - points: default=[], if empty list the refrigerant ph diagram is drawn.
              Points to be provided [p, t, x] with the mu [barg, degC, (0-1)],
              assign None to a value to skip it and calculate with the other two. 
              Points can be provided into a list or a dict:
        - list[list[float]], single thermodynamic cycle.
        - dict[str: list[float]], multiple thermodynamic cycles, the key of the dict is
                                  the cycle name in the graph.
    - pcrit: float [opt], critical pressure value, used instead of the value into the library [kPa] 
    - tcrit: float [opt], critical pressure value, used instead of the value into the library [degC]
    - plot_settings: dict, plot customizations
        - "xlim": list[float], x-axis limits
        - "ylim": list[float], y-axis limits
        - "figsize": list[float], default=(12, 12), figure size
    """
    N = 100 # number of points for saturation curves
    xlim = plot_settings.get('xlim')
    ylim = plot_settings.get('ylim')
    figsize = plot_settings.get('figsize', (12, 12))
    try:
        pcrit = PropsSI('Pcrit', ref) if pcrit is None else pcrit
        tcrit = PropsSI('Tcrit', ref) if tcrit is None else tcrit
        p_vap_liq = [pcrit * (i+1)/N for i in range(N)] + [pcrit]
        h_vap = [PropsSI('H', 'P', p, 'Q', 1, ref) for p in p_vap_liq]
        h_liq = [PropsSI('H', 'P', p, 'Q', 0, ref) for p in p_vap_liq]
        p_vap_liq = [p * 1e-5 for p in p_vap_liq]
        figure = plt.figure(figsize=figsize)
        plt.plot(h_vap, p_vap_liq, 'k', label="vap")
        plt.plot(h_liq, p_vap_liq, 'k', label="liq")
        if isinstance(points, list):
            p_cycle = []
            h_cycle = []
            if len(points) > 0:
                points.append(points[0])
                for point in points:
                    p, t, x, h = calc_h(point, ref)
                    p_cycle.append(p)
                    h_cycle.append(h)
            plt.plot(h_cycle, p_cycle, '-*', label="Cycle")
        elif isinstance(points, dict):
            for cycle in points:
                points_cycle = points[cycle]
                p_cycle = []
                h_cycle = []
                if len(points_cycle) > 0:
                    points_cycle.append(points_cycle[0])
                    for point in points_cycle:
                        p, t, x, h = calc_h(point, ref)
                        p_cycle.append(p)
                        h_cycle.append(h)
                plt.plot(h_cycle, p_cycle, '-*', label="Cycle")
        plt.xlabel("h [J/kg/K]")
        plt.ylabel("p [bar]")
        plt.yscale('log')
        plt.grid(which="both")
        if xlim:
            plt.xlim(xlim)
        if ylim:
            plt.ylim(ylim)
        plt.legend()
        plt.title(ref)
    
    except Exception as e:
        print(f"{e}\nIssue dealing with {ref} refrigerant.")

def R513a():
    "Create and return the R513a mixture to be used into PropsSI."
    R513a = 'R1234yf[0.56]&R134a[0.44]'
    CAS_R134a = CP.get_fluid_param_string('R134a','CAS')
    CAS_R1234yf = CP.get_fluid_param_string('R1234yf','CAS')
    try:
        CP.apply_simple_mixing_rule(CAS_R134a, CAS_R1234yf, 'linear')
    except Exception as e:
        print(R513a, 'already added to library\n\t', e)
    return R513a

def R515b():
    "Create and return the R515b mixture to be used into PropsSI."
    R515b = 'R1234ze(E)[0.911]&R227ea[0.089]'
    CAS_R1234zeE = CP.get_fluid_param_string('R1234ze(E)','CAS')
    CAS_R227ea = CP.get_fluid_param_string('R227ea','CAS')
    try:
        CP.apply_simple_mixing_rule(CAS_R1234zeE, CAS_R227ea, 'linear')
    except Exception as e:
        print(R515b, 'already added to library\n\t', e)
    return R515b
