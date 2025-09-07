-- include sfx 0 "m_tns_tetsudan_horn_1.ogg"
-- include sfx 1 "m_tns_tetsudan_horn_2.ogg"

RADIUS_INNER = 20
RADIUS_OUTER = 300
FADE_IN = 0.1 * 60
FADE_OUT = 0.5 * 60

function clamp(x, a, b)
	return math.min(math.max(x, a), b)
end

local play_state = {}
local volume_state = {}

function onTick()
	local composite, success = component.getInputLogicSlotComposite(0)
	if success then
		for i = 0, 1 do
			local b = composite.bool_values[i + 1]

			local v = volume_state[i] or 0
			v = clamp(clamp(b and 1 or 0, v - 1 / FADE_OUT, v + 1 / FADE_IN), 0, 1)
			volume_state[i] = v

			if v > 0 then
				if not play_state[i] then
					play_state[i] = component.sfxPlayLoop(i, i, 0, 0, 0, RADIUS_INNER, RADIUS_OUTER, v, 1, 2)
				else
					component.sfxUpdate(i, 0, 0, 0, RADIUS_INNER, RADIUS_OUTER, v, 1)
				end
			elseif component.sfxStop(i) then
				play_state[i] = false
			end
		end
	end
end

function onRemoveFromSimulation()
	for i = 0, 3 do
		component.sfxStop(i)
	end
end
