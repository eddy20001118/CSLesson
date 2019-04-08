# Projectile motion

## Tasks

### Code:

- Implemented by Python
- Portable, running on different platforms (Windows, Linux, macOS)
- Basic menu system:
  - enter system parameters and simulation properties
  - calculate simulation data
  - plot simulation data
  - save simulation data to file
  - 2-D graphic annimation

### Report:

- Introduction
- Specification
- Design
- Implementation
- Testing:
  - theory test
  - user input test
  - function/unit test
  - data verifying
  - platforms test
- Evaluation

## Theory

### Vector algorithms

#### Resolving vector:

The given vector m that has the magnitude m and direction (**given by the angle to the horizontal**) θ.
$$
m_x = m\cos{\theta}
$$

$$
m_y=msin{\theta}
$$

#### Resulting vector:

$$
m = \sqrt{m_x^2+m_y^2}
$$

### Acceleration

$$
a_y = g = \frac{F}{m} = \frac{GM}{r^2}
$$

### Velocity

#### General equation:

$$
v_y = v_{y0} + a_yt
$$

$$
v_x = v_{x0}
$$

#### Integration method:

$$
v_{xi} = v_{xi-1}
$$

$$
v_{yi} = v_{yi-1} + a_yT
$$



### Displacement

#### General equation:

$$
y = v_{y0}t + \frac{1}{2}a_yt^2
$$

$$
x = v_{x0}t
$$

#### Integration method:

$$
y_{i} = y_{i-1} + v_{yi}T
$$

$$
x_i = x_{i-1}+v_{xi}T
$$

