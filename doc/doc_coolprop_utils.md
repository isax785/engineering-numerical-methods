# DOC - CoolProp Utilities

- [DOC - CoolProp Utilities](#doc---coolprop-utilities)
  - [`ph` Diagram](#ph-diagram)
  - [Calculations](#calculations)
    - [`critical_point`](#critical_point)
    - [`calc_h`](#calc_h)
  - [Documentation](#documentation)

---

> `CoolProp` version: `6.4.1`

## `ph` Diagram

Drawing of one or multiple thermodynamic cycle on the refrigerant `ph` diagram.

```text
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
```

## Calculations

Calcualtion functions.

### `critical_point`

Printout of the Critical Point properties:

```text
  - ref: str, refrigerant id for CoolProp
```

### `calc_h`

Given two of three inputs among `[p, t, x]` the specific enthalpy `h` is returned.

```text
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
```

## Documentation

Functions that print useful informations:

- `propssi_usage_exaples`: prints some PropsSI usage examples;
- `measurement_units`: prints the measurement units of the mostly used magnitudes for refrigerants.


