from manim import *
import numpy as np


class TwoDWarp(Scene):
    def construct(self):
        blackhole=Dot(point=ORIGIN, color=BLACK).scale(3)
        glow=Circle(radius=0.3, color=WHITE).set_stroke(width=2)
        grid=NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            background_line_style={"stroke_opacity":0.4}
        )
        self.play(FadeIn(grid, glow, blackhole))
        particle=Dot(color=YELLOW).scale(0.5)
        def spiral_path(t):
            theta=8*t
            r=3*np.exp(-1.5*t)
            x=r*np.cos(theta)
            y=r*np.sin(theta)
            return np.array([x, y, 0])
        path_points=[spiral_path(t) for t in np.linspace(0, 2, 500)]
        path_line=VMobject(color=YELLOW)
        path_line.set_points_as_corners(path_points)
        self.play(Create(path_line), run_time=2, rate_func=linear)
        self.play(MoveAlongPath(particle, path_line), run_time=4, rate_func=linear)
        self.play(particle.animate.scale(0.1).move_to(ORIGIN), run_time=0.5)
        self.wait(1)
        self.play(FadeOut(grid, blackhole, glow, particle))


class WarpedSpacetime(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=70*DEGREES, theta=-45*DEGREES)

        title = Text("Spacetime Warping Near a Black Hole", font_size=36).to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        axes = ThreeDAxes(
            x_range=[-6, 6, 1],
            y_range=[-6, 6, 1],
            z_range=[-2, 2, 1],
            x_length=12,
            y_length=12,
            z_length=4,
            tips=False
        )
        self.play(Create(axes))

        r_s = 1.0
        grid_extent = 6

        def velocity(x):
            epsilon = 1e-6
            x = max(x, epsilon)
            return max(0, 1 - r_s / x)

        def get_velocity_from_radius(r):
            return min(1.0, 1.5 * (1 - r_s / max(r, r_s + 0.01)))

        blackhole = Sphere(radius=r_s, color=BLACK).move_to(ORIGIN)

        r_tracker = ValueTracker(5)
        velocity_label = always_redraw(lambda:
            VGroup(
                MathTex("v_{obs} = "),
                DecimalNumber(velocity(r_tracker.get_value()), num_decimal_places=2)
            ).arrange(RIGHT).to_corner(UR).scale(0.9)
        )
        self.add_fixed_in_frame_mobjects(velocity_label)
        self.add(velocity_label)

        def height_func(u, v):
            x, y = u, v
            epsilon = 0.1
            r = np.sqrt(x**2 + y**2 + epsilon)
            z = -(r_s / r) * 2
            return np.array([x, y, z])

        gravity_well = Surface(
            height_func,
            u_range=[-grid_extent, grid_extent],
            v_range=[-grid_extent, grid_extent],
            resolution=(50, 50),
            checkerboard_colors=[BLUE_D, BLUE_E],
            fill_opacity=0.7
        )
        self.play(Create(gravity_well))

        particle_radius = 0.1 * r_s
        particle = Sphere(radius=particle_radius, color=RED)
        start_pos = height_func(5, 0)
        particle.move_to(start_pos)
        self.add(particle)

        path = ParametricFunction(lambda t: height_func(5 - (5 - 1.1 * r_s) * t, 0), t_range=[0, 1])
        t_tracker = ValueTracker(0)
        self.add(t_tracker)
        def update_particle(mob):
            t = t_tracker.get_value()
            mob.move_to(path.point_from_proportion(t))
            r_tracker.set_value(abs(mob.get_center()[0]))

        particle.add_updater(update_particle)

        def update_t_tracker(dt):
            x = particle.get_center()[0]
            r = abs(x)
            speed = get_velocity_from_radius(r)
            new_value=min(1.0, t_tracker.get_value()+0.05*speed)
            t_tracker.set_value(new_value)
        
        t_tracker.add_updater(lambda m, dt: update_t_tracker(dt))
        self.wait(6)
        t_tracker.remove_updater(lambda m, dt: update_t_tracker(dt))
        particle.remove_updater(update_particle)
        self.wait(2)

        self.play(FadeOut(axes, gravity_well, particle, velocity_label))