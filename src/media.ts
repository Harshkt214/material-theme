const VIDEO_EXT = /\.(mp4|webm|mov|m4v|mkv)$/i;
export const isVideo = (src: string) => VIDEO_EXT.test(src);
