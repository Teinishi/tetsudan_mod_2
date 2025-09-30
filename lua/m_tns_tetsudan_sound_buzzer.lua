-- include sfx 0 "m_tns_tetsudan_buzzer_1.ogg"
-- include sfx 1 "m_tns_tetsudan_buzzer_2.ogg"
-- include sfx 2 "m_tns_tetsudan_buzzer_2_400.ogg"

RADIUS_INNER = 2
RADIUS_OUTER = 15

local play_state = {}

function onTick()
	local composite, success = component.getInputLogicSlotComposite(0)
	if success then
		for i = 0, 2 do
			local b = composite.bool_values[i + 1]

			if b and not play_state[i] then
				play_state[i] = component.sfxPlayOnce(i, i, 0, 0, 0, RADIUS_INNER, RADIUS_OUTER, 1, 1, 2)
			elseif not b and component.sfxStop(i) then
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
