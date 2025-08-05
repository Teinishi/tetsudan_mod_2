-- include sfx 0 "m_tns_tetsudan_controller_type1_1.ogg"
-- include sfx 1 "m_tns_tetsudan_controller_type1_2.ogg"

local PIVOT = {0, 0.05, 0}
local STEP_START = -9
local STEP_POS = {
	{0, 0.125, 0.072169},
	{0, 0.125, 0.057831},
	{0, 0.125, 0.047831},
	{0, 0.125, 0.038831},
	{0, 0.125, 0.029831},
	{0, 0.125, 0.021831},
	{0, 0.125, 0.013831},
	{0, 0.125, 0.005831},
	{0, 0.125, -0.002169},
	{0, 0.125, -0.012},
	{0, 0.125, -0.022169},
	{0, 0.125, -0.032169},
	{0, 0.125, -0.043169},
	{0, 0.125, -0.057169},
	{0, 0.125, -0.072169},
}

local step_angles = {}
for i, v in ipairs(STEP_POS) do
	step_angles[i + STEP_START - 1] = math.atan(v[3] - PIVOT[3], v[2] - PIVOT[2])
end

local ppos = nil
local transform = matrix.identity()

function onTick()
	local value, success = component.getInputLogicSlotFloat(index)
	if success then
		local pos = math.min(math.max(math.floor(value + 0.5), STEP_START), STEP_START + #STEP_POS - 1)
		if ppos ~= nil and pos ~= ppos then
			if pos == 0 or ppos == 0 or pos == STEP_START or ppos == STEP_START then
				component.sfxPlayOnce(1, 1, 0, 0, 0, 1, 6, 1, 1, 0.5)
			end
			component.sfxPlayOnce(0, 0, 0, 0, 0, 1, 6, 1, 1, 0.5)
		end
		ppos = pos
		transform = matrix.multiply(
			matrix.translation(PIVOT[1], PIVOT[2], PIVOT[3]),
			matrix.rotationX(step_angles[pos])
		)
	end
end

function onRender()
	component.renderMesh0(transform)
end
