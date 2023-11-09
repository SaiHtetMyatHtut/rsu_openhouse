<script>
	let videoSource = null;
    let base_url = "https://b155-34-125-52-110.ngrok-free.app"
    let image;
	const toggleCamera = async () => {
		try {
			if (videoSource.srcObject) {
				videoSource.srcObject.getTracks().forEach((track) => track.stop());
				videoSource.srcObject = null;
			} else {
				const stream = await navigator.mediaDevices.getUserMedia({
					video: { facingMode: { exact: 'environment' }, width: 500, height: 500 }
				});
				videoSource.srcObject = stream;
				videoSource.style.transform = 'scaleX(-1)'; // This line flips the video horizontally
				videoSource.play();
			}
		} catch (error) {
			console.log(error);
		}
	};

	const takePicture = async () => {
		try {
			const canvas = document.createElement('canvas');
			canvas.width = videoSource.videoWidth;
			canvas.height = videoSource.videoHeight;
			const context = canvas.getContext('2d');
			context.translate(canvas.width, 0);
			context.scale(-1, 1); // Flip the image horizontally
			context.drawImage(videoSource, 0, 0, canvas.width, canvas.height);
			const dataURL = canvas.toDataURL('image/png');
			const blob = await (await fetch(dataURL)).blob();
			const file = new File([blob], 'image.png');
			toggleCamera();

			let formData = new FormData();
			formData.append('image', file);
			const response = await fetch(base_url+'/image', {
				method: 'POST',
				body: formData
			});
			if (response.status !== 200) {
				throw new Error('Network response was not ok');
			}
            let data = await response.json();
			console.log(data.file_name);
            
            const imageResponse = await fetch(base_url+"/get/"+data.file_name);
            if (imageResponse.status !== 200) {
                throw new Error('Network response was not ok');
            }
            console.log(imageResponse);
            image.src = await imageResponse.url;

		} catch (error) {
			console.log(error);
		}
	};
</script>

<header class="h-28 w-screen" />
<div class="w-screen h-80 flex justify-center pt-10">
	<video class="w-80 h-80" bind:this={videoSource}>
		<track kind="captions" />
	</video>
    <img  bind:this={image} alt="">
</div>
<div class="pb-10 pt-20 text-center">
	<h1
		class="mx-auto max-w-4xl font-display text-5xl font-medium tracking-tight text-slate-900 sm:text-7xl"
	>
		Your
		<span class="relative whitespace-nowrap text-blue-600">
			<svg
				aria-hidden="true"
				viewBox="0 0 418 42"
				class="absolute left-0 top-2/3 h-[0.58em] w-full fill-blue-300/70"
				preserveAspectRatio="none"
			/>
			<span class="relative">Alternative</span>
		</span>{' '}
		Reality
	</h1>
	<p class="mx-auto mt-6 max-w-2xl text-lg tracking-tight text-slate-700">
		Click take picture to get preview and transform to alternative reality
	</p>
	<div class="mt-10 flex justify-center gap-x-6">
		<button
			on:click={takePicture}
			class="group inline-flex items-center justify-center rounded-full py-2 px-4 text-sm font-semibold focus:outline-none focus-visible:outline-2 focus-visible:outline-offset-2 bg-blue-600 text-white hover:text-slate-100 hover:bg-blue-500 active:bg-blue-800 active:text-blue-100 focus-visible:outline-blue-600"
		>
			Take Picture
		</button>
		<button
			on:click={toggleCamera}
			class="group inline-flex ring-1 items-center justify-center rounded-full py-2 px-4 text-sm focus:outline-none ring-slate-200 text-slate-700 hover:text-slate-900 hover:ring-slate-300 active:bg-slate-100 active:text-slate-600 focus-visible:outline-blue-600 focus-visible:ring-slate-300"
		>
			<svg aria-hidden="true" class="h-3 w-3 flex-none fill-blue-600 group-active:fill-current">
				<path
					d="m9.997 6.91-7.583 3.447A1 1 0 0 1 1 9.447V2.553a1 1 0 0 1 1.414-.91L9.997 5.09c.782.355.782 1.465 0 1.82Z"
				/>
			</svg>
			<span class="ml-3">Preview</span>
		</button>
	</div>
</div>