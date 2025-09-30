RADIUS_INNER = 20
RADIUS_OUTER = 200

local function clamp(x, a, b)
	return math.min(math.max(x, a), b)
end

local sfx_channel = {}
local channels_not_in_use, channels_in_use = {0, 1, 2, 3}, {}

local function stop_channel(channel)
	if component.sfxStop(channel) then
		for i, v in ipairs(channels_in_use) do
			if v == channel then
				table.remove(channels_in_use, i)
				table.insert(channels_not_in_use, channel)
				return true
			end
		end
	end
	return false
end

local function allocate_channel()
	if #channels_not_in_use == 0 then
		stop_channel(channels_in_use[1])
	end
	if #channels_not_in_use > 0 then
		local channel = table.remove(channels_not_in_use, 1)
		table.insert(channels_in_use, channel)
		return channel
	else
		return nil
	end
end

local function sfx_update(i, volume, pitch, is_once)
	if volume > 0 then
		if sfx_channel[i] == nil then
			local channel = allocate_channel()
			if channel ~= nil then
				local fn = is_once and component.sfxPlayOnce or component.sfxPlayLoop
				if fn(channel, i - 1, 0, 0, 0, RADIUS_INNER, RADIUS_OUTER, volume, pitch, 1) then
					sfx_channel[i] = channel
				end
			end
		else
			component.sfxUpdate(sfx_channel[i], 0, 0, 0, RADIUS_INNER, RADIUS_OUTER, volume, pitch)
		end
	elseif volume <= 0 and sfx_channel[i] ~= nil then
		if stop_channel(sfx_channel[i]) then
			sfx_channel[i] = nil
		end
	end
end

function onTick()
	local composite, success = component.getInputLogicSlotComposite(0)
	if success then
		local fv = composite.float_values
		for i = 1, #BASE_SPEED do
			local volume, speed = clamp(fv[2 * i - 1], 0, 1), fv[2 * i]
			local base = BASE_SPEED[i]
			if base ~= nil then
				sfx_update(i, volume, 3.6 * speed / base, ONCE)
			end
		end
	end
end

function onRemoveFromSimulation()
	for i = 0, 3 do
		stop_channel(i)
	end
end
