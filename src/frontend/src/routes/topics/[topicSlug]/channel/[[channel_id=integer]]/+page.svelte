<script lang="ts">
    import { page } from "$app/stores";
    import { fetchApi } from "$lib/api.js";
    import { messageStore } from "$lib/stores/";
    import Message from "./message.svelte";
    import type { TopicChatMessageInterface } from "$lib/types";
    import MessageInput from "./messageInput.svelte";

    export let data;

    $: selectedChannelId = $page.params.channel_id;
    $: messages = ($messageStore[data.channel?.id ?? -1] ?? {}).results;

    $: {
        if (data.channel && messages === undefined) {
            fetchApi(`channels/${data.channel!.id}/messages/`).then((response) => {
                response.json().then((fetchedMessages) => {
                    messageStore.update((msgs) => {
                        msgs[data.channel!.id] = fetchedMessages;
                        return msgs;
                    });
                });
            });
        }
    }

    let isFetchingNewMessages = false;

    function loadMessages(event: Event) {
        if (!data.channel || !messages) {
            return;
        }

        const element = event.target as HTMLDivElement;

        if (element.scrollHeight + element.scrollTop < 750) {
            if (
                !isFetchingNewMessages &&
                messages.length !== $messageStore[data.channel!.id].count
            ) {
                isFetchingNewMessages = true;
                fetchApi(
                    `channels/${data.channel!.id}/messages/?before=${
                        messages[messages.length - 1].id
                    }`
                ).then((response) => {
                    if (response.ok) {
                        response.json().then((data) => {
                            messageStore.update((existingMessages) => {
                                existingMessages[data.channel!.id].results?.push(...data.results);
                                return existingMessages;
                            });
                            isFetchingNewMessages = false;
                        });
                    }
                });
            }
        }
    }

    function getIsInlineMsg(idx: number, message: TopicChatMessageInterface): boolean {
        const msg = ($messageStore[data.channel!.id]?.results ?? [])[idx + 1];

        if (msg?.author?.id === message?.author.id) {
            const prevMsgCreatedAt = Date.parse(msg.created_at);
            const currentMsgCreatedAt = Date.parse(message.created_at);

            // Calculate the time gap between the 3 messages in seconds
            const diffInSeconds = Math.floor((currentMsgCreatedAt - prevMsgCreatedAt) / 1000);

            // if the time gap between the 2 messages is more than 5 minutes, it is not an inline message
            if (diffInSeconds > 300) {
                return false;
            }

            return true;
        }

        return false;
    }

    let messageContent = "";

    async function sendMessage(event: Event) {
        event.preventDefault(); // If this is not called the input will lose focus

        const finalMessageContent = messageContent.trim();

        if (!!data.channel && finalMessageContent) {
            const response = await fetchApi(`channels/${data.channel.id}/messages/`, {
                method: "POST",
                body: JSON.stringify({ content: finalMessageContent })
            });

            if (response.ok) {
                messageContent = "";
            }
        }
    }
</script>

{#if !selectedChannelId}
    <h1 class="text-3xl text-center font-semibold mt-[20dvh]">Select a channel to view</h1>
{:else if data.channel === undefined}
    Loading...
{:else if data.channel === null}
    404 channel not found
{:else}
    <div
        class="flex flex-col justify-end bg-discordDark-730 max-h-[calc(100vh-var(--navbar-height))] h-full scroll-smooth pb-1 w-full"
    >
        <div
            class="flex border-b border-discordDark-600 items-center gap-2 text-lg font-medium
				   pl-8 py-3"
        >
            <span>
                {data.topic.name}
            </span>
            <svg
                xmlns="http://www.w3.org/2000/svg"
                height="14px"
                fill="currentColor"
                viewBox="0 0 384 512"
                ><!--! Font Awesome Free 6.4.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path
                    d="M3.4 81.7c-7.9 15.8-1.5 35 14.3 42.9L280.5 256 17.7 387.4C1.9 395.3-4.5 414.5 3.4 430.3s27.1 22.2 42.9 14.3l320-160c10.8-5.4 17.7-16.5 17.7-28.6s-6.8-23.2-17.7-28.6l-320-160c-15.8-7.9-35-1.5-42.9 14.3z"
                /></svg
            >
            <span>
                {data.channel.name}
            </span>
        </div>

        <div class="channel-messages" on:scroll={loadMessages}>
            {#each messages || [] as message, idx (message.id)}
                {@const isInlineMsg = getIsInlineMsg(idx, message)}
                <Message {message} isInline={isInlineMsg} />
            {/each}
        </div>

        <form on:submit={sendMessage} class="px-4">
            <MessageInput bind:value={messageContent} />
        </form>
    </div>
{/if}

<style lang="scss">
    .channel-messages {
        @apply overflow-y-auto h-full p-2 flex flex-col-reverse;
    }
</style>