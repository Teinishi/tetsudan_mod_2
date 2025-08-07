function clamp(x, a, b)
	return math.min(math.max(x, a), b)
end

function lerp(a, b, t)
	return a*(1 - t) + b*t
end

local smooth = true
local t = 1
local transform = matrix.identity()

function update(t_tgt)
	if not inserted and value ~= 1 then
		smooth = true
	elseif inserted and t == t_tgt then
		smooth = false
	end
	t = smooth and clamp(t_tgt, t - 0.05, t + 0.05) or t_tgt
	local theta = lerp(90, -60, t)/180*math.pi
	transform = matrix.rotationY(theta)
end

function onParse()
	t, _ = parser.parseNumber("t", t)
	update(t)
end

function onTick()
	local composite, success = component.getInputLogicSlotComposite(0)
	if success then
		local inserted = composite.bool_values[1]
		local value = composite.float_values[1]
		update(inserted and clamp(value, 0, 1) or 0.9)
	end
end

function onRender()
	component.renderMesh0(transform)
end
