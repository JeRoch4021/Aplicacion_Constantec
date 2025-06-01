import React, { useState } from 'react'
import {
  Box,
  Text,
  Callout,
  Button,
} from '@radix-ui/themes'
import ReactPlayer from 'react-player/youtube'

export const Tutorial = () => {
    return (
        <Box width="700px" mt="2" style={{ display: 'flex', justifyContent: 'center' }}>
            <Box
                style={{
                    background: '#fff',
                    borderRadius: 16,
                    boxShadow: '0 4px 24px rgba(0,0,0,0.10)',
                    padding: 24,
                    maxWidth: 700,
                    width: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                }}
            >
                <Text size="3" weight="bold" align="center">
                    Video Tutorial
                </Text>
                <Box
                    style={{
                        borderRadius: 12,
                        overflow: 'hidden',
                        border: '2px solid #e5e7eb',
                        boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
                        width: '100%',
                        maxWidth: 560,
                        aspectRatio: '16/9',
                        background: '#000',
                        display: 'flex',
                        justifyContent: 'center',
                        alignItems: 'center',
                    }}
                >
                    <ReactPlayer
                        url='https://www.youtube.com/watch?v=Kcy9S94kYgI'
                        controls={true}
                        width="100%"
                        height="100%"
                        style={{ borderRadius: 12 }}
                    />
                </Box>
            </Box>
        </Box>
    )
}
