document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('user-input');
    const charCount = document.getElementById('char-count');
    const targetSelect = document.getElementById('target-select');
    const convertButton = document.getElementById('convert-button');
    const convertedOutput = document.getElementById('converted-output');
    const copyButton = document.getElementById('copy-button');

    const MAX_CHARS = 500;

    // 1. Character Count
    if (userInput && charCount) {
        userInput.addEventListener('input', () => {
            const currentLength = userInput.value.length;
            charCount.textContent = `${currentLength}/${MAX_CHARS}자`;
            // The maxlength attribute already handles truncation.
        });
        // Initialize char count on load
        charCount.textContent = `${userInput.value.length}/${MAX_CHARS}자`;
    }

    // 2. Convert Button Logic
    if (convertButton && userInput && targetSelect && convertedOutput) {
        convertButton.addEventListener('click', async () => {
            const textToConvert = userInput.value;
            const targetAudience = targetSelect.value;

            if (textToConvert.trim() === '') {
                alert('변환할 내용을 입력해주세요.');
                return;
            }

            // Disable button and show loading state
            convertButton.disabled = true;
            convertButton.textContent = '변환 중...';
            convertButton.classList.add('opacity-50', 'cursor-not-allowed');
            convertedOutput.value = '변환 중입니다. 잠시만 기다려 주세요...';

            try {
                const response = await fetch('/convert', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ text: textToConvert, target: targetAudience }),
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || '알 수 없는 오류가 발생했습니다.');
                }

                const data = await response.json();
                convertedOutput.value = data.convertedText;
            } catch (error) {
                console.error('Conversion failed:', error);
                convertedOutput.value = `오류가 발생했습니다: ${error.message}. 잠시 후 다시 시도해주세요.`;
            } finally {
                // Re-enable button
                convertButton.disabled = false;
                convertButton.textContent = '변환하기';
                convertButton.classList.remove('opacity-50', 'cursor-not-allowed');
            }
        });
    }

    // 3. Copy Button Logic
    if (copyButton && convertedOutput) {
        copyButton.addEventListener('click', async () => {
            if (convertedOutput.value.trim() === '') {
                // You might want to provide a small, non-blocking notification here instead of an alert
                return;
            }

            try {
                await navigator.clipboard.writeText(convertedOutput.value);
                
                // Provide visual feedback
                const originalText = copyButton.textContent;
                copyButton.textContent = '복사 완료!';
                copyButton.classList.remove('bg-gray-600', 'hover:bg-gray-700');
                copyButton.classList.add('bg-green-500', 'hover:bg-green-600');

                setTimeout(() => {
                    copyButton.textContent = originalText;
                    copyButton.classList.remove('bg-green-500', 'hover:bg-green-600');
                    copyButton.classList.add('bg-gray-600', 'hover:bg-gray-700');
                }, 2000);
            } catch (err) {
                console.error('Failed to copy: ', err);
                alert('클립보드 복사에 실패했습니다.');
            }
        });
    }
});