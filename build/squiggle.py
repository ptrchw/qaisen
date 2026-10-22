"""Design-thinking 'squiggle': a tangled scribble on the left that unwinds into a
straight line on the right. viewBox 1440 x 240, baseline y=210."""
import math, random
random.seed(5)
W, H, YB = 1440, 240, 210

def noise(seed_terms):
    def f(t):
        return sum(a * math.sin(fr * t + ph) for a, fr, ph in seed_terms)
    return f
def terms(n, fmin, fmax):
    return [(random.uniform(.4, 1) / n, random.uniform(fmin, fmax), random.uniform(0, 6.28)) for _ in range(n)]

nr, ny, nth, ncx = noise(terms(4, 3, 19)), noise(terms(4, 3, 23)), noise(terms(3, 2, 9)), noise(terms(3, 4, 15))
pts = []
# 1) the tangle — overlapping, irregular loops that shrink as the line moves right
N1 = 1600
x_start, x_end = 150, 600
for i in range(N1 + 1):
    t = i / N1
    env = (1 - t) ** 1.35                      # overall size shrinks to the right
    cx = x_start + (x_end - x_start) * (t ** 1.5) + 85 * env * ncx(t * 9)
    theta = 2 * math.pi * 30 * t + 3.4 * nth(t * 7)
    rx = (14 + 118 * env) * (0.65 + 0.6 * abs(nr(t * 11)) + 0.2)
    ry = (10 + 104 * env) * (0.6 + 0.55 * abs(ny(t * 9)) + 0.2)
    cy = YB - ry * 0.7 - 18 * env * nr(t * 13)
    pts.append((cx + rx * math.cos(theta), cy - ry * math.sin(theta)))
# 2) loose waves settling down
x0, y0 = pts[-1]
N2 = 260
for i in range(1, N2 + 1):
    t = i / N2
    x = x0 + (930 - x0) * t
    amp = 26 * (1 - t) ** 1.8
    y = YB + (y0 - YB) * (1 - t) ** 4 - amp * abs(math.sin(2 * math.pi * 4.5 * t)) * (1 + 0.3 * math.sin(17 * t))
    pts.append((x, y))
pts.append((W + 40, YB))
# keep everything inside the viewBox
pts = [(x, max(6, min(y, YB + 4))) for x, y in pts]
d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
open(__file__.replace("squiggle.py", "squiggle_path.txt"), "w").write(d)
print(len(d), min(y for _, y in pts))
