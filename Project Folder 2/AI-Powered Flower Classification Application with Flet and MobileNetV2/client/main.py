import flet as ft
import websockets
import base64
import json
import io

def main(page: ft.Page):
    page.title = "Flower Classification"
    page.scroll = "adaptive"
    page.window.width = 800
    page.window.height = 500
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    image_holder = ft.Image(
        src=f"upload_flower.png",
        width=100,
        height=100,
        # fit=ft.ImageFit.CONTAIN,
        fit="contain",

    )    
    result_text = ft.Text(value="Awaiting image...")
    
    # 2. Async handler for clicking the image container
    async def handle_loaded_file(e):
        filepick = ft.FilePicker()
        page.overlay.append(filepick)
        # Await the file picker directly
        files = await filepick.pick_files(
            allow_multiple=False, 
            allowed_extensions=['jpg', 'png', 'jpeg']
        )
        
        # files will be None if the user cancels the dialog
        if files and len(files) > 0:
            file_path = files[0].path
            print(f"Selected: {file_path}")

            # Display the image locally using the absolute path
            image_holder.src = file_path
            image_holder.width = 230  # Expand to fit the container
            image_holder.height = 230
            page.update()

    # 3. Async handler for clicking the Predict button
    async def predict_image(e):
        if image_holder.src and image_holder.src != "upload_flower.png":
            # Read the image data from the local file path
            with open(image_holder.src, "rb") as image_file:
                image_bytes = image_file.read()
                image_data = base64.b64encode(image_bytes).decode("utf-8")

            # Await the prediction directly (No asyncio.run needed!)
            result_text.value = "Predicting..."
            page.update()
            await send_prediction_request(image_data)
        else:
            print("No image selected")
            result_text.value = "Please select an image first."
            page.update()

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
                    result_msg = f"Predicted Class: {data.get('class')}\nScore: {round(data.get('score'), 2)}"
                    result_text.value = result_msg
                    
                    # Update the specific container content
                    selected_image.controls[2].content.value = result_msg
                else:
                    error_msg = "Error occurred during prediction"
                    result_text.value = error_msg
                    selected_image.controls[2].content.value = error_msg
                
                page.update()
                
        except Exception as err:
            print(f"An unexpected error occurred: {err}")
            result_text.value = "Failed to connect to server."
            page.update()
        finally:
            print("Prediction request finished.")

    # UI Layout
    selected_image = ft.Row(
        [
           
           
           
            # Container now triggers handle_loaded_file directly
            ft.Container(
                content=image_holder,
                margin=10,
                padding=10,
                border=ft.Border.all(5, ft.Colors.BLACK),
                alignment=ft.Alignment.CENTER,
                bgcolor=ft.Colors.WHITE,
                width=250,
                height=250,
                border_radius=10,
                ink=True,
                on_click=handle_loaded_file,  # <-- Attached the async function here!
            ),
            ft.Container(
                content=ft.Image(
                    src=f"arrowtotheright.png",
                    height=160,                    
                    fit="contain",

                ),
                bgcolor=ft.Colors.YELLOW,                    
            ),

             ft.Container(
                content=result_text,
                margin=10,
                padding=10,
                border=ft.Border.all(5, ft.Colors.BLACK),
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
        ft.Button(content="Predict", width=150, height=50, on_click= predict_image),
        alignment=ft.Alignment.CENTER,
    )
    
    page.add(
        selected_image,
        predict_button
    )

# ft.app(target=main)
# ft.run(main)
ft.run(main, assets_dir="assets", upload_dir="assets/uploads")