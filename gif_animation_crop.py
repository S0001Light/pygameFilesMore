import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageSequence


class GifCropper:
    def __init__(self, root):
        self.root = root
        self.root.title("Animated GIF Cropper")
        self.root.geometry("1000x750")
        self.root.minsize(700, 500)

        # GIF data
        self.gif_path = None
        self.original_frames = []
        self.frame_durations = []
        self.loop_count = 0

        # Preview data
        self.preview_frames = []
        self.preview_index = 0
        self.animation_job = None

        # Display scaling
        self.display_scale = 1.0
        self.display_width = 0
        self.display_height = 0

        # Selection information
        self.start_x = None
        self.start_y = None
        self.crop_rectangle = None
        self.crop_box = None

        self.create_interface()

    def create_interface(self):
        toolbar = tk.Frame(self.root, padx=8, pady=8)
        toolbar.pack(fill=tk.X)

        tk.Button(
            toolbar,
            text="Open GIF",
            width=14,
            command=self.open_gif
        ).pack(side=tk.LEFT, padx=4)

        tk.Button(
            toolbar,
            text="Select All",
            width=14,
            command=self.select_all
        ).pack(side=tk.LEFT, padx=4)

        tk.Button(
            toolbar,
            text="Clear Selection",
            width=14,
            command=self.clear_selection
        ).pack(side=tk.LEFT, padx=4)

        tk.Button(
            toolbar,
            text="Save Cropped GIF",
            width=18,
            command=self.save_cropped_gif
        ).pack(side=tk.LEFT, padx=4)

        self.info_label = tk.Label(
            toolbar,
            text="Open an animated GIF to begin.",
            anchor="w"
        )
        self.info_label.pack(side=tk.LEFT, padx=14)

        canvas_container = tk.Frame(self.root, bg="#292929")
        canvas_container.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(
            canvas_container,
            bg="#202020",
            highlightthickness=0,
            cursor="crosshair"
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.selection_start)
        self.canvas.bind("<B1-Motion>", self.selection_drag)
        self.canvas.bind("<ButtonRelease-1>", self.selection_end)
        self.canvas.bind("<Configure>", self.canvas_resized)

        self.status_label = tk.Label(
            self.root,
            text="Drag over the GIF to select the crop region.",
            anchor="w",
            relief=tk.SUNKEN,
            padx=8
        )
        self.status_label.pack(fill=tk.X)

    def open_gif(self):
        path = filedialog.askopenfilename(
            title="Open Animated GIF",
            filetypes=[
                ("GIF images", "*.gif"),
                ("All files", "*.*")
            ]
        )

        if not path:
            return

        try:
            self.stop_animation()

            gif = Image.open(path)

            if getattr(gif, "n_frames", 1) < 1:
                raise ValueError("The GIF contains no readable frames.")

            self.gif_path = path
            self.loop_count = gif.info.get("loop", 0)

            self.original_frames.clear()
            self.frame_durations.clear()

            default_duration = gif.info.get("duration", 100)

            # Convert every frame to RGBA to preserve composited frame data.
            for frame in ImageSequence.Iterator(gif):
                rgba_frame = frame.convert("RGBA").copy()
                self.original_frames.append(rgba_frame)

                duration = frame.info.get("duration", default_duration)

                # Very small or missing durations can animate badly.
                if not duration or duration < 10:
                    duration = 100

                self.frame_durations.append(duration)

            gif.close()

            self.crop_box = None
            self.preview_index = 0

            self.build_preview_frames()
            self.draw_current_frame()
            self.start_animation()

            width, height = self.original_frames[0].size

            self.info_label.config(
                text=(
                    f"{len(self.original_frames)} frames | "
                    f"{width} x {height} pixels"
                )
            )

            self.status_label.config(
                text="Drag on the animation to select an area to crop."
            )

        except Exception as error:
            messagebox.showerror(
                "Open GIF Error",
                f"Could not open the GIF:\n\n{error}"
            )

    def canvas_resized(self, event):
        if not self.original_frames:
            return

        self.build_preview_frames()
        self.draw_current_frame()

        if self.crop_box:
            self.draw_crop_rectangle_from_original_box()

    def build_preview_frames(self):
        if not self.original_frames:
            return

        canvas_width = max(self.canvas.winfo_width(), 1)
        canvas_height = max(self.canvas.winfo_height(), 1)

        image_width, image_height = self.original_frames[0].size

        padding = 30

        available_width = max(canvas_width - padding, 1)
        available_height = max(canvas_height - padding, 1)

        scale_x = available_width / image_width
        scale_y = available_height / image_height

        # Do not enlarge small GIFs above their original size.
        self.display_scale = min(scale_x, scale_y, 1.0)

        self.display_width = max(
            1,
            round(image_width * self.display_scale)
        )
        self.display_height = max(
            1,
            round(image_height * self.display_scale)
        )

        self.preview_frames.clear()

        for frame in self.original_frames:
            resized = frame.resize(
                (self.display_width, self.display_height),
                Image.Resampling.LANCZOS
            )
            self.preview_frames.append(ImageTk.PhotoImage(resized))

    def get_image_position(self):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        image_x = (canvas_width - self.display_width) // 2
        image_y = (canvas_height - self.display_height) // 2

        return image_x, image_y

    def draw_current_frame(self):
        if not self.preview_frames:
            return

        self.canvas.delete("gif_frame")

        image_x, image_y = self.get_image_position()

        self.canvas.create_image(
            image_x,
            image_y,
            anchor=tk.NW,
            image=self.preview_frames[self.preview_index],
            tags="gif_frame"
        )

        # Keep crop rectangle above the frame.
        if self.crop_rectangle:
            self.canvas.tag_raise(self.crop_rectangle)

    def start_animation(self):
        self.stop_animation()
        self.animate_next_frame()

    def stop_animation(self):
        if self.animation_job is not None:
            self.root.after_cancel(self.animation_job)
            self.animation_job = None

    def animate_next_frame(self):
        if not self.preview_frames:
            return

        self.draw_current_frame()

        duration = self.frame_durations[self.preview_index]

        self.preview_index += 1
        if self.preview_index >= len(self.preview_frames):
            self.preview_index = 0

        self.animation_job = self.root.after(
            max(duration, 10),
            self.animate_next_frame
        )

    def clamp_to_image(self, canvas_x, canvas_y):
        image_x, image_y = self.get_image_position()

        clamped_x = max(
            image_x,
            min(canvas_x, image_x + self.display_width)
        )

        clamped_y = max(
            image_y,
            min(canvas_y, image_y + self.display_height)
        )

        return clamped_x, clamped_y

    def point_is_inside_image(self, canvas_x, canvas_y):
        image_x, image_y = self.get_image_position()

        return (
            image_x <= canvas_x <= image_x + self.display_width
            and image_y <= canvas_y <= image_y + self.display_height
        )

    def selection_start(self, event):
        if not self.original_frames:
            return

        if not self.point_is_inside_image(event.x, event.y):
            return

        self.start_x, self.start_y = self.clamp_to_image(
            event.x,
            event.y
        )

        self.crop_box = None

        if self.crop_rectangle:
            self.canvas.delete(self.crop_rectangle)

        self.crop_rectangle = self.canvas.create_rectangle(
            self.start_x,
            self.start_y,
            self.start_x,
            self.start_y,
            outline="#00ff66",
            width=2,
            dash=(6, 3)
        )

    def selection_drag(self, event):
        if self.start_x is None or self.start_y is None:
            return

        current_x, current_y = self.clamp_to_image(
            event.x,
            event.y
        )

        self.canvas.coords(
            self.crop_rectangle,
            self.start_x,
            self.start_y,
            current_x,
            current_y
        )

        self.update_status_from_canvas_box(
            self.start_x,
            self.start_y,
            current_x,
            current_y
        )

    def selection_end(self, event):
        if self.start_x is None or self.start_y is None:
            return

        end_x, end_y = self.clamp_to_image(event.x, event.y)

        left = min(self.start_x, end_x)
        top = min(self.start_y, end_y)
        right = max(self.start_x, end_x)
        bottom = max(self.start_y, end_y)

        self.start_x = None
        self.start_y = None

        if right - left < 2 or bottom - top < 2:
            self.clear_selection()
            return

        self.crop_box = self.canvas_box_to_original_box(
            left,
            top,
            right,
            bottom
        )

        self.draw_crop_rectangle_from_original_box()
        self.update_crop_status()

    def canvas_box_to_original_box(self, left, top, right, bottom):
        image_x, image_y = self.get_image_position()
        original_width, original_height = self.original_frames[0].size

        original_left = round(
            (left - image_x) / self.display_scale
        )
        original_top = round(
            (top - image_y) / self.display_scale
        )
        original_right = round(
            (right - image_x) / self.display_scale
        )
        original_bottom = round(
            (bottom - image_y) / self.display_scale
        )

        original_left = max(0, min(original_left, original_width - 1))
        original_top = max(0, min(original_top, original_height - 1))
        original_right = max(1, min(original_right, original_width))
        original_bottom = max(1, min(original_bottom, original_height))

        return (
            original_left,
            original_top,
            original_right,
            original_bottom
        )

    def original_box_to_canvas_box(self, crop_box):
        image_x, image_y = self.get_image_position()
        left, top, right, bottom = crop_box

        canvas_left = image_x + left * self.display_scale
        canvas_top = image_y + top * self.display_scale
        canvas_right = image_x + right * self.display_scale
        canvas_bottom = image_y + bottom * self.display_scale

        return (
            canvas_left,
            canvas_top,
            canvas_right,
            canvas_bottom
        )

    def draw_crop_rectangle_from_original_box(self):
        if not self.crop_box:
            return

        canvas_box = self.original_box_to_canvas_box(self.crop_box)

        if self.crop_rectangle:
            self.canvas.coords(self.crop_rectangle, *canvas_box)
        else:
            self.crop_rectangle = self.canvas.create_rectangle(
                *canvas_box,
                outline="#00ff66",
                width=2,
                dash=(6, 3)
            )

        self.canvas.tag_raise(self.crop_rectangle)

    def update_status_from_canvas_box(
        self,
        left,
        top,
        right,
        bottom
    ):
        crop_box = self.canvas_box_to_original_box(
            min(left, right),
            min(top, bottom),
            max(left, right),
            max(top, bottom)
        )

        x1, y1, x2, y2 = crop_box

        self.status_label.config(
            text=(
                f"Selection: X={x1}, Y={y1}, "
                f"Width={x2 - x1}, Height={y2 - y1}"
            )
        )

    def update_crop_status(self):
        if not self.crop_box:
            return

        left, top, right, bottom = self.crop_box

        self.status_label.config(
            text=(
                f"Crop region: X={left}, Y={top}, "
                f"Width={right - left}, Height={bottom - top}"
            )
        )

    def select_all(self):
        if not self.original_frames:
            return

        width, height = self.original_frames[0].size
        self.crop_box = (0, 0, width, height)

        self.draw_crop_rectangle_from_original_box()
        self.update_crop_status()

    def clear_selection(self):
        self.crop_box = None
        self.start_x = None
        self.start_y = None

        if self.crop_rectangle:
            self.canvas.delete(self.crop_rectangle)
            self.crop_rectangle = None

        if self.original_frames:
            self.status_label.config(
                text="Selection cleared. Drag to select a crop region."
            )

    def save_cropped_gif(self):
        if not self.original_frames:
            messagebox.showwarning(
                "No GIF",
                "Open an animated GIF first."
            )
            return

        if not self.crop_box:
            messagebox.showwarning(
                "No Crop Selection",
                "Drag over the GIF to select the crop region."
            )
            return

        output_path = filedialog.asksaveasfilename(
            title="Save Cropped Animated GIF",
            defaultextension=".gif",
            filetypes=[
                ("GIF images", "*.gif"),
                ("All files", "*.*")
            ]
        )

        if not output_path:
            return

        try:
            cropped_frames = []

            for frame in self.original_frames:
                cropped = frame.crop(self.crop_box)
                cropped_frames.append(cropped)

            if not cropped_frames:
                raise ValueError("No animation frames were available.")

            first_frame = cropped_frames[0]
            remaining_frames = cropped_frames[1:]

            first_frame.save(
                output_path,
                format="GIF",
                save_all=True,
                append_images=remaining_frames,
                duration=self.frame_durations,
                loop=self.loop_count,
                disposal=2,
                optimize=False
            )

            width = self.crop_box[2] - self.crop_box[0]
            height = self.crop_box[3] - self.crop_box[1]

            messagebox.showinfo(
                "GIF Saved",
                (
                    "The cropped animated GIF was saved successfully.\n\n"
                    f"Frames: {len(cropped_frames)}\n"
                    f"Output size: {width} x {height}\n\n"
                    f"{output_path}"
                )
            )

        except Exception as error:
            messagebox.showerror(
                "Save Error",
                f"Could not save the cropped GIF:\n\n{error}"
            )

    def close(self):
        self.stop_animation()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = GifCropper(root)

    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()


if __name__ == "__main__":
    main()
