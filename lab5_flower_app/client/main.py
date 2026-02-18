import flet as ft
import websockets
import asyncio
import base64
import json
from PIL import Image
import io
import re
import tempfile

def main(page: ft.Page):
    page.title = "Flower Classification"
    page.scroll = "adaptive"
    page.window.width = 800
    page.window.height = 500
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER

    image_holder = ft.Image(src="https://flet.dev/img/logo.svg", visible=False, width=250, height=250)
    result_text = ft.Text()

    def handle_loaded_file(e):
        if e.files and len(e.files):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                with open(e.files[0].path, "rb") as image_file:
                    temp_file.write(image_file.read())

            image_holder.src = temp_file.name
            image_holder.visible = True
            page.update()

            file_path = e.files[0].path
            print(file_path)

            img = Image.open(file_path)
            byte_io = io.BytesIO()
            img.save(byte_io, 'PNG')
            byte_io.seek(0)
            image_bytes = byte_io.read()
            image_data = base64.b64encode(image_bytes).decode("utf-8")

    filepick = ft.FilePicker()
    filepick.on_result = handle_loaded_file
    page.overlay.append(filepick)

    def predict_image(e):
        if image_holder.src:
            with open(image_holder.src, "rb") as image_file:
                image_bytes = image_file.read()
                image_data = base64.b64encode(image_bytes).decode("utf-8")
            asyncio.run(send_prediction_request(image_data))
        else:
            print("No image selected")

    async def send_prediction_request(image_data):
        try:
            async with websockets.connect("ws://localhost:8000/ws") as websocket:
                await websocket.send(json.dumps({
                    "type": "predict",
                    "data": image_data
                }))

                response = await websocket.recv()
                data = json.loads(response)

                if data.get("type") == "prediction":
                    result_text.value = f"Predicted Class: {data.get('class')}"
                    selected_image.controls[2].content.value = (
                        f"Predicted Class: {data.get('class')}"
                        + f"\nScore: {round(data.get('score'), 2)}"
                    )
                    page.update()
                else:
                    result_text.value = "Error occurred during prediction"
                    selected_image.controls[2].content.value = "Error occurred during prediction"
                    page.update()

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            print("Make sure the server is running")

    selected_image = ft.Row(
        [
            ft.Container(
                content=image_holder,
                margin=10,
                padding=10,
                border=ft.border.all(5, ft.Colors.BLACK),
                alignment=ft.Alignment.CENTER,
                bgcolor=ft.Colors.WHITE,
                width=250,
                height=250,
                border_radius=10,
                ink=True,
                on_click=lambda _: filepick.pick_files(
                    allow_multiple=False,
                    allowed_extensions=['jpg', 'png', 'jpeg']
                ),
            ),
            ft.Container(
                content=ft.Image(
                    src="arrowtotheright.png",
                    height=160,
                    fit=ft.image,
                )
            ),
            ft.Container(
                content=result_text,
                margin=10,
                padding=10,
                border=ft.border.all(5, ft.Colors.BLACK),
                alignment=ft.Alignment.CENTER,
                bgcolor=ft.Colors.WHITE,
                width=300,
                height=125,
                border_radius=10,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    predict_button = ft.Container(
            ft.Button(content="Predict", width=150, height=50, on_click=predict_image),
            alignment=ft.Alignment.CENTER,
        ),
        
    page.add(
        result_text,
        selected_image,
        predict_button
    )

ft.run(main)
