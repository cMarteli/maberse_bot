
import unittest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from DailyMessage import send_daily_message, start

class TestDailyMessage(unittest.TestCase):

    @patch('MyJokes.tell_joke', new_callable=AsyncMock)
    @patch('Weather.getweather', new_callable=AsyncMock)
    def test_send_daily_message(self, mock_getweather, mock_tell_joke):
        # Arrange
        mock_bot = MagicMock()
        mock_channel = AsyncMock()
        mock_bot.get_channel.return_value = mock_channel
        
        mock_tell_joke.return_value = "Why did the scarecrow win an award? Because he was outstanding in his field."
        mock_getweather.return_value = 25
        
        channel_id = 12345

        # Act
        asyncio.run(send_daily_message(mock_bot, channel_id))

        # Assert
        mock_bot.get_channel.assert_called_with(channel_id)
        
        expected_message = (
            "**Daily Update!**\n\n"
            "Here is your daily joke:\nWhy did the scarecrow win an award? Because he was outstanding in his field.\n\n"
            "The current weather in Perth is 25°C."
        )
        mock_channel.send.assert_called_with(expected_message)

    @patch('DailyMessage.AsyncIOScheduler')
    def test_start_scheduler(self, mock_scheduler):
        # Arrange
        mock_bot = MagicMock()
        channel_id = 12345
        
        # Act
        start(mock_bot, channel_id)

        # Assert
        mock_scheduler.assert_called_with()
        mock_scheduler.return_value.add_job.assert_called_once()
        mock_scheduler.return_value.start.assert_called_once()


if __name__ == '__main__':
    unittest.main()
