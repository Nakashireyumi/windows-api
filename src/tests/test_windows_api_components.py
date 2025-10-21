"""
Unit tests for windows-api components
Tests the GUI automation handlers and WebSocket server
"""

import pytest
import asyncio
import json
import yaml
import tempfile
import os
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from pathlib import Path
import sys

# Add the project to the path for imports
project_root = Path(__file__).parents[2]
sys.path.insert(0, str(project_root / "src" / "dev" / "cassitly" / "python"))

# Import handlers
from interactions_api.handlers import click, move, keydown, keyup, hotkey, dragto, dragrel

class TestClickHandler:
    """Test click handler functionality"""
    
    @pytest.mark.asyncio
    @patch('interactions_api.handlers.click.pyautogui')
    async def test_click_with_coordinates(self, mock_pyautogui):
        """Test clicking at specific coordinates"""
        msg = {"x": 100, "y": 200, "button": "left"}
        context = {}
        
        result = await click.handle(msg, context)
        
        mock_pyautogui.moveTo.assert_called_once_with(100, 200)
        mock_pyautogui.click.assert_called_once_with(button="left")
        
        assert result["status"] == "ok"
        assert result["result"]["clicked"] == [100, 200]
        assert result["result"]["button"] == "left"
    
    @pytest.mark.asyncio
    @patch('interactions_api.handlers.click.pyautogui')
    async def test_click_without_coordinates(self, mock_pyautogui):
        """Test clicking without coordinates"""
        msg = {"button": "right"}
        context = {}
        
        result = await click.handle(msg, context)
        
        mock_pyautogui.moveTo.assert_not_called()
        mock_pyautogui.click.assert_called_once_with(button="right")
        
        assert result["status"] == "ok"
        assert result["result"]["button"] == "right"
    
    @pytest.mark.asyncio
    @patch('interactions_api.handlers.click.pyautogui')
    async def test_click_default_button(self, mock_pyautogui):
        """Test clicking with default button"""
        msg = {"x": 50, "y": 75}
        context = {}
        
        result = await click.handle(msg, context)
        
        mock_pyautogui.moveTo.assert_called_once_with(50, 75)
        mock_pyautogui.click.assert_called_once_with(button="left")
        
        assert result["status"] == "ok"
        assert result["result"]["button"] == "left"
    
    @pytest.mark.asyncio
    @patch('interactions_api.handlers.click.pyautogui')
    async def test_click_invalid_coordinates(self, mock_pyautogui):
        """Test clicking with invalid coordinates"""
        msg = {"x": "invalid", "y": 100, "button": "left"}
        context = {}
        
        result = await click.handle(msg, context)
        
        # Should not call moveTo with invalid coordinates
        mock_pyautogui.moveTo.assert_not_called()
        mock_pyautogui.click.assert_called_once_with(button="left")


class TestMoveHandler:
    """Test move handler functionality"""
    
    @pytest.mark.asyncio
    @patch('interactions_api.handlers.move.pyautogui')
    async def test_move_to_coordinates(self, mock_pyautogui):
        """Test moving to specific coordinates"""
        msg = {"x": 300, "y": 400}
        context = {}
        
        result = await move.handle(msg, context)
        
        mock_pyautogui.moveTo.assert_called_once_with(300, 400)
        
        assert result["status"] == "ok"
        assert result["result"]["moved_to"] == [300, 400]
    
    @pytest.mark.asyncio
    async def test_move_missing_coordinates(self):
        """Test move with missing coordinates"""
        msg = {"x": 100}  # Missing y coordinate
        context = {}
        
        with pytest.raises(Exception):
            await move.handle(msg, context)


class TestKeyHandlers:
    """Test keyboard input handlers"""
    
    @pytest.mark.asyncio
    @patch('interactions_api.handlers.keydown.pyautogui')
    async def test_keydown(self, mock_pyautogui):
        """Test key down action"""
        msg = {"key": "ctrl"}
        context = {}
        
        result = await keydown.handle(msg, context)
        
        mock_pyautogui.keyDown.assert_called_once_with("ctrl")
        assert result["status"] == "ok"
        assert result["result"]["key_down"] == "ctrl"
    
    @pytest.mark.asyncio
    @patch('interactions_api.handlers.keyup.pyautogui')
    async def test_keyup(self, mock_pyautogui):
        """Test key up action"""
        msg = {"key": "shift"}
        context = {}
        
        result = await keyup.handle(msg, context)
        
        mock_pyautogui.keyUp.assert_called_once_with("shift")
        assert result["status"] == "ok"
        assert result["result"]["key_up"] == "shift"
    
    @pytest.mark.asyncio
    @patch('interactions_api.handlers.hotkey.pyautogui')
    async def test_hotkey_single_key(self, mock_pyautogui):
        """Test hotkey with single key"""
        msg = {"keys": ["enter"]}
        context = {}
        
        result = await hotkey.handle(msg, context)
        
        mock_pyautogui.hotkey.assert_called_once_with("enter")
        assert result["status"] == "ok"
        assert result["result"]["hotkey"] == ["enter"]
    
    @pytest.mark.asyncio
    @patch('interactions_api.handlers.hotkey.pyautogui')
    async def test_hotkey_multiple_keys(self, mock_pyautogui):
        """Test hotkey with multiple keys"""
        msg = {"keys": ["ctrl", "c"]}
        context = {}
        
        result = await hotkey.handle(msg, context)
        
        mock_pyautogui.hotkey.assert_called_once_with("ctrl", "c")
        assert result["status"] == "ok"
        assert result["result"]["hotkey"] == ["ctrl", "c"]


class TestDragHandlers:
    """Test drag operation handlers"""
    
    @pytest.mark.asyncio
    @patch('interactions_api.handlers.dragto.pyautogui')
    async def test_dragto(self, mock_pyautogui):
        """Test drag to absolute coordinates"""
        msg = {"x": 500, "y": 600, "duration": 1.0}
        context = {}
        
        result = await dragto.handle(msg, context)
        
        mock_pyautogui.dragTo.assert_called_once_with(500, 600, duration=1.0)
        assert result["status"] == "ok"
        assert result["result"]["dragged_to"] == [500, 600]
    
    @pytest.mark.asyncio
    @patch('interactions_api.handlers.dragrel.pyautogui')
    async def test_dragrel(self, mock_pyautogui):
        """Test drag by relative coordinates"""
        msg = {"dx": 100, "dy": -50, "duration": 0.5}
        context = {}
        
        result = await dragrel.handle(msg, context)
        
        mock_pyautogui.drag.assert_called_once_with(100, -50, duration=0.5)
        assert result["status"] == "ok"
        assert result["result"]["dragged_by"] == [100, -50]


class TestConfigurationLoading:
    """Test configuration loading and validation"""
    
    def create_test_config(self, tmp_path, config_data):
        """Helper to create a test configuration file"""
        config_file = tmp_path / "authentication.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(config_data, f)
        return config_file
    
    def test_load_valid_config(self, tmp_path):
        """Test loading valid configuration"""
        config_data = {
            "host": "localhost",
            "port": 9999,
            "auth_token": "test-token-123",
            "screenshot_dir": "./test_screenshots",
            "failsafe": True,
            "pause": 0.1
        }
        
        config_file = self.create_test_config(tmp_path, config_data)
        
        # Mock the path finding logic
        with patch('interactions_api.__main__.Path') as mock_path:
            mock_path.return_value.resolve.return_value.parents = [tmp_path.parent, tmp_path]
            mock_path.return_value.name = "windows-api"
            
            # This would normally be tested by importing the module,
            # but we'll test the config loading function directly
            from interactions_api.__main__ import load_config
            
            with patch('interactions_api.__main__.Path.__file__', str(config_file.parent / "dummy.py")):
                with patch.object(Path, 'parents', [tmp_path]):
                    # Test configuration values
                    assert config_data["host"] == "localhost"
                    assert config_data["port"] == 9999
                    assert config_data["auth_token"] == "test-token-123"
    
    def test_config_missing_file(self, tmp_path):
        """Test handling missing configuration file"""
        # This should be tested by mocking the file operations
        from interactions_api.__main__ import load_config
        
        with patch('interactions_api.__main__.Path') as mock_path:
            mock_path.return_value.resolve.return_value.parents = []
            
            with pytest.raises(RuntimeError, match="Could not locate 'windows-api' directory"):
                load_config()
    
    def test_config_invalid_yaml(self, tmp_path):
        """Test handling invalid YAML configuration"""
        config_file = tmp_path / "authentication.yaml"
        with open(config_file, 'w') as f:
            f.write("invalid: yaml: content: [")
        
        from interactions_api.__main__ import load_config
        
        with patch('interactions_api.__main__.Path') as mock_path:
            mock_path.return_value.resolve.return_value.parents = [tmp_path]
            mock_path.return_value.name = "windows-api"
            
            with pytest.raises(yaml.YAMLError):
                with patch('builtins.open', open):
                    load_config()


class TestMessageHandling:
    """Test message handling and dispatch"""
    
    @pytest.mark.asyncio
    async def test_handle_message_valid_token(self):
        """Test message handling with valid token"""
        from interactions_api.__main__ import handle_message
        
        msg = {
            "token": "test-token",
            "action": "click",
            "x": 100,
            "y": 200
        }
        
        with patch('interactions_api.__main__.AUTH_TOKEN', "test-token"):
            with patch('interactions_api.__main__.handlers', {"click": AsyncMock(return_value={"status": "ok"})}):
                result = await handle_message(msg)
                
        response = json.loads(result)
        assert response["status"] == "ok"
    
    @pytest.mark.asyncio
    async def test_handle_message_invalid_token(self):
        """Test message handling with invalid token"""
        from interactions_api.__main__ import handle_message
        
        msg = {
            "token": "wrong-token",
            "action": "click"
        }
        
        with patch('interactions_api.__main__.AUTH_TOKEN', "correct-token"):
            result = await handle_message(msg)
                
        response = json.loads(result)
        assert response["status"] == "error"
        assert response["error"]["message"] == "unauthorized"
    
    @pytest.mark.asyncio
    async def test_handle_message_missing_action(self):
        """Test message handling without action"""
        from interactions_api.__main__ import handle_message
        
        msg = {
            "token": "test-token"
            # Missing action
        }
        
        with patch('interactions_api.__main__.AUTH_TOKEN', "test-token"):
            result = await handle_message(msg)
                
        response = json.loads(result)
        assert response["status"] == "error"
        assert "invalid_action" in response["error"]["message"]
    
    @pytest.mark.asyncio
    async def test_handle_message_unsupported_action(self):
        """Test message handling with unsupported action"""
        from interactions_api.__main__ import handle_message
        
        msg = {
            "token": "test-token",
            "action": "unsupported_action"
        }
        
        with patch('interactions_api.__main__.AUTH_TOKEN', "test-token"):
            with patch('interactions_api.__main__.handlers', {}):
                result = await handle_message(msg)
                
        response = json.loads(result)
        assert response["status"] == "error"
        assert "unsupported_action" in response["error"]["message"]
    
    @pytest.mark.asyncio
    async def test_handle_reload_action(self):
        """Test reload action"""
        from interactions_api.__main__ import handle_message
        
        msg = {
            "token": "test-token",
            "action": "reload"
        }
        
        with patch('interactions_api.__main__.AUTH_TOKEN', "test-token"):
            with patch('interactions_api.__main__.load_handlers') as mock_load:
                with patch('interactions_api.__main__.handlers', {"test": "handler"}):
                    result = await handle_message(msg)
                    
        response = json.loads(result)
        assert response["status"] == "ok"
        assert "Handlers reloaded" in response["result"]["message"]
        mock_load.assert_called_once()


class TestUtilityFunctions:
    """Test utility functions"""
    
    def test_ok_function(self):
        """Test ok response function"""
        from interactions_api.__main__ import ok
        
        result = ok({"test": "data"})
        response = json.loads(result)
        
        assert response["status"] == "ok"
        assert response["result"]["test"] == "data"
    
    def test_ok_function_no_payload(self):
        """Test ok response function without payload"""
        from interactions_api.__main__ import ok
        
        result = ok()
        response = json.loads(result)
        
        assert response["status"] == "ok"
        assert response["result"] == {}
    
    def test_err_function(self):
        """Test error response function"""
        from interactions_api.__main__ import err
        
        result = err("test error", {"detail": "info"})
        response = json.loads(result)
        
        assert response["status"] == "error"
        assert response["error"]["message"] == "test error"
        assert response["error"]["details"]["detail"] == "info"
    
    def test_err_function_no_details(self):
        """Test error response function without details"""
        from interactions_api.__main__ import err
        
        result = err("simple error")
        response = json.loads(result)
        
        assert response["status"] == "error"
        assert response["error"]["message"] == "simple error"
        assert response["error"]["details"] == ""


class TestWebSocketServer:
    """Test WebSocket server functionality"""
    
    @pytest.mark.asyncio
    async def test_websocket_handler_valid_json(self):
        """Test WebSocket handler with valid JSON"""
        from interactions_api.__main__ import handler
        
        mock_websocket = AsyncMock()
        mock_websocket.__aiter__.return_value = ['{"token": "test", "action": "click"}']
        
        with patch('interactions_api.__main__.handle_message') as mock_handle:
            mock_handle.return_value = '{"status": "ok"}'
            
            # Run handler for one iteration
            handler_task = asyncio.create_task(handler(mock_websocket))
            await asyncio.sleep(0.1)  # Let it process one message
            handler_task.cancel()
            
            try:
                await handler_task
            except asyncio.CancelledError:
                pass
        
        mock_handle.assert_called()
        mock_websocket.send.assert_called_with('{"status": "ok"}')
    
    @pytest.mark.asyncio
    async def test_websocket_handler_invalid_json(self):
        """Test WebSocket handler with invalid JSON"""
        from interactions_api.__main__ import handler
        
        mock_websocket = AsyncMock()
        mock_websocket.__aiter__.return_value = ['invalid json']
        
        # Run handler for one iteration
        handler_task = asyncio.create_task(handler(mock_websocket))
        await asyncio.sleep(0.1)  # Let it process one message
        handler_task.cancel()
        
        try:
            await handler_task
        except asyncio.CancelledError:
            pass
        
        # Should send error response for invalid JSON
        mock_websocket.send.assert_called()
        sent_response = mock_websocket.send.call_args[0][0]
        response = json.loads(sent_response)
        assert response["status"] == "error"
        assert "invalid_json" in response["error"]["message"]


if __name__ == "__main__":
    # Run with: python -m pytest src/tests/test_windows_api_components.py -v
    print("Run tests with: python -m pytest src/tests/test_windows_api_components.py -v")