<script>
	let videoSource = null;
	let base_url = 'http://171.248.247.140:56192';
	let image_url = '';
	let overlay_url = '';
	let showImageOverlay = false;
	let isLoading = false;
	let isCameraOn = false;
	let isFinished = false;
	let gender = 'male';
	let prompt = "";

	async function generateQRCode(data) {
		let qrGeneratorUrl = 'https://api.qrserver.com/v1/create-qr-code/?size=512x512&data=' + data;
		let qrCodeImageUrl = qrGeneratorUrl;
		const response = await fetch(qrCodeImageUrl);
		if (response.status !== 200) {
			throw new Error('Network response was not ok');
		}
		const blob = await response.blob();
		overlay_url = URL.createObjectURL(blob);
	}

	const toggleCamera = async () => {
		try {
			if (videoSource && videoSource.srcObject) {
				isCameraOn = false;
				videoSource.srcObject.getTracks().forEach((track) => track.stop());
				videoSource.srcObject = null;
			} else {
				isCameraOn = true;
				const stream = await navigator.mediaDevices.getUserMedia({
					video: { facingMode: 'environment' },
					audio: false
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
			isLoading = true;

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
			formData.append('raw_image', file);
			const response = await fetch(base_url + '/image?is_boy='+gender+"&prompt="+prompt, {
				method: 'POST',
				body: formData
			});
			if (response.status !== 200) {
				throw new Error('Network response was not ok');
			}
			let data = await response.json();
			console.log(data.file_name);

			const imageResponse = await fetch(base_url + '/get/' + data.file_name);
			if (imageResponse.status !== 200) {
				throw new Error('Network response was not ok');
			}
			console.log(imageResponse);
			image_url = await imageResponse.url;
			generateQRCode(image_url);
			// image.src = image_url
			isFinished = true;
		} catch (error) {
			console.log(error);
		} finally {
			isLoading = false;
		}
	};
</script>

<header class="h-28 w-screen" />
<div class="w-screen h-80 flex justify-center pt-10">
	{#if isLoading && !isCameraOn}
		<div class="w-80 h-80 flex items-center justify-center">
			<div class="relative m-auto">
				<div class="h-24 w-24 rounded-full border-t-8 border-b-8 border-gray-200" />
				<div
					class="absolute top-0 left-0 h-24 w-24 rounded-full border-t-8 border-b-8 border-blue-500 animate-spin"
				/>
			</div>
		</div>
	{:else if isCameraOn}
		<video
			bind:this={videoSource}
			class="w-80 h-80"
			autoplay
			playsinline
			muted
			style="transform: scaleX(-1);"
		/>
	{:else if !image_url}
		<img
			class="w-80 h-80 rounded-md"
			alt=""
			src="https://media.tenor.com/7UDr7ANLiSEAAAAd/cats-kitty.gif"
			autoplay
		/>
	{:else}
		{#if showImageOverlay}
			<div
				class="fixed top-0 left-0 w-screen h-screen flex items-center justify-center bg-black bg-opacity-80 z-50 rounded-md"
			>
				<img class="max-w-full max-h-full rounded-md" src={overlay_url} alt="overlay" />
			</div>
		{/if}
		<img
			class="w-80 h-80 rounded-md"
			src={image_url}
			alt="original"
			autoplay
			on:click={() => (showImageOverlay = true)}
		/>
	{/if}
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
	<input
		bind:value={prompt}
		class="mx-auto my-5 w-[400px] bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
		type="text"
		placeholder="What's do you want to become."
	/>
	<div class="mt-10 flex-col justify-center gap-x-6">
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
		<div class="mt-5 flex justify-center gap-x-6">
			<button
				on:click={() => (gender = 'male')}
				class={`group inline-flex items-center justify-center rounded-full py-2 px-4 text-sm font-semibold focus:outline-none focus-visible:outline-2 focus-visible:outline-offset-2 ${
					gender === 'male' ? 'bg-red-600 text-white' : 'text-slate-700'
				}  hover:text-slate-100 hover:bg-slate-500 active:bg-slate-800 active:text-blue-100 focus-visible:outline-blue-600`}
			>
				Male
			</button>
			<button
				on:click={() => (gender = 'female')}
				class={`group inline-flex items-center justify-center rounded-full py-2 px-4 text-sm font-semibold focus:outline-none focus-visible:outline-2 focus-visible:outline-offset-2 ${
					gender === 'female' ? 'bg-red-600 text-white' : 'text-slate-700'
				}  hover:text-slate-100 hover:bg-slate-500 active:bg-slate-800 active:text-blue-100 focus-visible:outline-blue-600`}
			>
				Female
			</button>
		</div>
	</div>
</div>
